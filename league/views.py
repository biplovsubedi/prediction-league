from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests
from django.utils import timezone
from django.shortcuts import render
from rest_framework import generics, pagination, status, views
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ActualStanding, Gameweek, Player, Prediction, Score, Team, SiteState
from .serializers import PlayerSerializer, ScoreSerializer, TeamSerializer


FPL_BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"



class ScoreListView(generics.ListAPIView):
    serializer_class = ScoreSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        qs = Score.objects.select_related("player", "player__favourite_team").order_by(
            "-score_correct", "score_deviation"
        )
        player_type = self.request.query_params.get("player_type")
        if player_type in {"normal", "pundit"}:
            qs = qs.filter(player__player_type=player_type)
        return qs


@method_decorator(cache_page(600), name="dispatch")
class CurrentPLStandingsView(views.APIView):
    def get(self, request):
        resp = requests.get(FPL_BOOTSTRAP_URL, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        teams = data.get("teams", [])
        simplified = [
            {
                "id": t.get("id"),
                "name": t.get("name"),
                "short_name": t.get("short_name"),
                "win": t.get("win", 0),
                "loss": t.get("loss", 0),
                "draw": t.get("draw", 0),
                "points": t.get("points", 0),
                "position": t.get("position", 0),
            }
            for t in teams
        ]
        simplified.sort(key=lambda x: x.get("position") or 0)
        return Response(simplified)


def _compute_scores_for_gameweek(current_gw: Gameweek, season: str) -> None:
    predictions = (
        Prediction.objects.select_related("player", "team")
        .filter(season=season)
        .all()
    )

    actuals = {
        (a.team_id): a
        for a in ActualStanding.objects.filter(season=season, gameweek=current_gw.id)
    }

    # Aggregate by player
    by_player: Dict[int, Dict[str, int]] = {}
    for p in predictions:
        a = actuals.get(p.team_id)
        if not a:
            continue
        stats = by_player.setdefault(p.player_id, {
            "score_correct": 0,
            "score_deviation": 0,
            "rank_correct": 0,
            "rank_deviation": 0,
        })
        if p.predicted_rank == a.actual_rank:
            stats["score_correct"] += 1
            stats["rank_correct"] += 1
        deviation = abs(int(p.predicted_rank) - int(a.actual_rank))
        stats["score_deviation"] += deviation
        stats["rank_deviation"] += deviation

    # Write Score rows
    for player_id, stats in by_player.items():
        Score.objects.update_or_create(
            season=season,
            gameweek=current_gw.id,
            player_id=player_id,
            defaults={
                **stats,
                "completed": current_gw.finished and current_gw.data_checked,
            },
        )


class UpdateScoresView(views.APIView):
    """Trigger to update teams, gameweeks, actual standings and compute scores.

    Debounce if last run within 24 hours (stored in a singleton row via Gameweek flags).
    """

    def post(self, request):
        season = request.data.get("season", "2025/26")

        # Debounce using SiteState.last_computed timestamp
        state, _ = SiteState.objects.get_or_create(id=1)
        if state.last_computed and (timezone.now() - state.last_computed) < timedelta(hours=24):
            return Response({"status": "skipped_recent_run"})

        # Fetch bootstrap-static
        resp = requests.get(FPL_BOOTSTRAP_URL, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        # Upsert teams
        for t in data.get("teams", []):
            Team.objects.update_or_create(
                id=t["id"],
                defaults={
                    "name": t.get("name", ""),
                    "short_name": t.get("short_name", ""),
                    "code": t.get("code", 0),
                },
            )

        # Upsert gameweeks
        current_gw: Optional[Gameweek] = None
        for ev in data.get("events", []):
            gw, _ = Gameweek.objects.update_or_create(
                id=ev["id"],
                defaults={
                    "is_current": ev.get("is_current", False),
                    "finished": ev.get("finished", False),
                    "data_checked": ev.get("data_checked", False),
                },
            )
            if gw.is_current:
                current_gw = gw

        # Update actual standings from teams object
        if current_gw is None:
            # best effort choose latest finished or id 1
            current_gw = Gameweek.objects.order_by("-is_current", "id").first()

        teams = data.get("teams", [])
        for t in teams:
            ActualStanding.objects.update_or_create(
                season=season,
                gameweek=current_gw.id if current_gw else 1,
                team_id=t["id"],
                defaults={
                    "actual_rank": t.get("position", 0) or 0,
                    "points": t.get("points", 0) or 0,
                },
            )

        if current_gw:
            _compute_scores_for_gameweek(current_gw, season)

        # mark debounce
        state.last_computed = timezone.now()
        state.save(update_fields=["last_computed"])

        return Response({"status": "ok", "season": season})


@api_view(["GET"])
def health(_request):
    return Response({"status": "ok"})


# HTML pages
def pl_table(request):
    return render(request, "league/pl_standings.html")


def current_standings_page(request):
    return render(request, "league/current_standings.html")


class ScoreCurrentView(views.APIView):
    def get(self, request):
        player_type = request.GET.get("player_type")
        # choose current gw as latest finished+checked else is_current
        gw = (
            Gameweek.objects.filter(finished=True, data_checked=True).order_by("-id").first()
            or Gameweek.objects.filter(is_current=True).order_by("-id").first()
        )
        prev_gw = None
        if gw:
            prev_gw = (
                Gameweek.objects.filter(id__lt=gw.id, finished=True, data_checked=True)
                .order_by("-id")
                .first()
            )

        def fetch_scores(gw_obj: Optional[Gameweek]):
            if not gw_obj:
                return []
            qs = Score.objects.select_related("player", "player__favourite_team").filter(gameweek=gw_obj.id)
            if player_type in {"normal", "pundit"}:
                qs = qs.filter(player__player_type=player_type)
            return list(qs)

        current_scores = fetch_scores(gw)
        previous_scores = fetch_scores(prev_gw)

        def build_rank_map(scores: List[Score], key_correct, key_deviation):
            # rank for correct-based (desc), then deviation-based (asc)
            sorted_correct = sorted(scores, key=key_correct, reverse=True)
            rank_correct = {}
            last_val = None
            rank = 0
            for idx, s in enumerate(sorted_correct, start=1):
                val = key_correct(s)
                if val != last_val:
                    rank = idx
                    last_val = val
                rank_correct[s.player_id] = rank

            sorted_dev = sorted(scores, key=key_deviation)
            rank_dev = {}
            last_val = None
            rank = 0
            for idx, s in enumerate(sorted_dev, start=1):
                val = key_deviation(s)
                if val != last_val:
                    rank = idx
                    last_val = val
                rank_dev[s.player_id] = rank
            return rank_correct, rank_dev

        key_correct = lambda s: (s.score_correct, -s.score_deviation)
        key_deviation = lambda s: (s.score_deviation, -s.score_correct)
        curr_rank_correct_map, curr_rank_dev_map = build_rank_map(current_scores, key_correct, key_deviation)
        prev_rank_correct_map, prev_rank_dev_map = build_rank_map(previous_scores, key_correct, key_deviation)

        payload = []
        for s in current_scores:
            payload.append(
                {
                    "username": s.player.username,
                    "player_type": s.player.player_type,
                    "team_name": s.player.favourite_team.name if s.player.favourite_team else None,
                    "gameweek": s.gameweek,
                    "score_correct": s.score_correct,
                    "score_deviation": s.score_deviation,
                    "curr_rank_correct_based": curr_rank_correct_map.get(s.player_id),
                    "curr_rank_deviation_based": curr_rank_dev_map.get(s.player_id),
                    "last_rank_correct_based": prev_rank_correct_map.get(s.player_id),
                    "last_rank_deviation_based": prev_rank_dev_map.get(s.player_id),
                }
            )

        return Response({"gameweek": gw.id if gw else None, "results": payload})


class UserHistoryView(views.APIView):
    def get(self, request, username: str):
        season = request.GET.get("season", "2025/26")
        player = Player.objects.filter(username=username).first()
        if not player:
            return Response({"username": username, "results": []})
        scores = (
            Score.objects.filter(player=player, season=season)
            .order_by("gameweek")
            .all()
        )
        results = [
            {
                "gameweek": s.gameweek,
                "score_correct": s.score_correct,
                "score_deviation": s.score_deviation,
                "rank_correct": s.rank_correct,
                "rank_deviation": s.rank_deviation,
                "completed": s.completed,
            }
            for s in scores
        ]
        return Response({
            "username": player.username,
            "player_type": player.player_type,
            "team_name": player.favourite_team.name if player.favourite_team else None,
            "season": season,
            "results": results,
        })


def user_history_page(request, username: str):
    return render(request, "league/user_history.html", {"username": username})


def homepage(request):
    return render(request, "league/home.html")

# Create your views here.
