from rest_framework import serializers

from .models import Player, Score, Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "short_name", "code"]


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["username", "player_type"]


class ScoreSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)

    class Meta:
        model = Score
        fields = [
            "season",
            "gameweek",
            "player",
            "score_correct",
            "score_deviation",
            "rank_correct",
            "rank_deviation",
            "completed",
        ]


