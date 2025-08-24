from django.db import models
from django.core.validators import MinValueValidator


class Team(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    code = models.PositiveIntegerField()

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.name


class Gameweek(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    is_current = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    data_checked = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"GW {self.id}"


class Player(models.Model):
    PLAYER_TYPES = (
        ("normal", "Normal"),
        ("pundit", "Pundit"),
    )

    username = models.CharField(max_length=100, unique=True)
    custom_team_name = models.CharField(max_length=100, blank=True, null=True, help_text="User's custom team name")
    player_type = models.CharField(max_length=10, choices=PLAYER_TYPES, default="normal")

    def __str__(self) -> str:
        return self.username


class Prediction(models.Model):
    season = models.CharField(max_length=9, default="2025/26")
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    predicted_rank = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1, message="Predicted rank must be at least 1")]
    )

    class Meta:
        unique_together = [
            ("season", "player", "predicted_rank"),
            ("season", "player", "team")
        ]
        indexes = [
            models.Index(fields=["season", "player"]),
        ]

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.predicted_rank == 0:
            raise ValidationError("Predicted rank cannot be 0")
        if self.predicted_rank is None:
            raise ValidationError("Predicted rank cannot be null")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class ActualStanding(models.Model):
    season = models.CharField(max_length=9, default="2025/26")
    gameweek = models.PositiveSmallIntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    actual_rank = models.PositiveSmallIntegerField()
    points = models.PositiveIntegerField(default=0)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("season", "gameweek", "team")
        indexes = [
            models.Index(fields=["season", "gameweek"]),
        ]


class Score(models.Model):
    season = models.CharField(max_length=9, default="2025/26")
    gameweek = models.PositiveSmallIntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score_correct = models.PositiveSmallIntegerField(default=0)
    score_deviation = models.PositiveIntegerField(default=0)
    rank_correct = models.PositiveSmallIntegerField(default=0)
    rank_deviation = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("season", "gameweek", "player")
        indexes = [
            models.Index(fields=["season", "gameweek"]),
        ]


class SiteState(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1)
    last_computed = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Site State"
        verbose_name_plural = "Site State"

# Create your models here.
