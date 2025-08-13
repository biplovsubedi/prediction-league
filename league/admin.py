from django.contrib import admin
from .models import Team, Gameweek, Player, Prediction, ActualStanding, Score, SiteState


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "short_name", "code")
    search_fields = ("name", "short_name")


@admin.register(Gameweek)
class GameweekAdmin(admin.ModelAdmin):
    list_display = ("id", "is_current", "finished", "data_checked")
    list_filter = ("is_current", "finished", "data_checked")


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("username", "player_type", "favourite_team")
    list_filter = ("player_type",)
    search_fields = ("username",)


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("season", "player", "team", "predicted_rank")
    list_filter = ("season",)
    search_fields = ("player__username", "team__name")


@admin.register(ActualStanding)
class ActualStandingAdmin(admin.ModelAdmin):
    list_display = ("season", "gameweek", "team", "actual_rank", "points", "updated_time")
    list_filter = ("season", "gameweek")


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        "season",
        "gameweek",
        "player",
        "score_correct",
        "score_deviation",
        "rank_correct",
        "rank_deviation",
        "completed",
    )
    list_filter = ("season", "gameweek", "completed")


@admin.register(SiteState)
class SiteStateAdmin(admin.ModelAdmin):
    list_display = ("id", "last_computed")

# Register your models here.
