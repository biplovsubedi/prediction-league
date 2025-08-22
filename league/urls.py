from django.urls import path

from .views import (
    CurrentPLStandingsView,
    ScoreListView,
    UpdateScoresView,
    ScoreCurrentView,
    UserHistoryView,
    UserPredictionsView,
    current_standings_page,
    user_history_page,
    homepage,
    health,
    pl_table,
)


urlpatterns = [
    path("", homepage),
    path("health/", health),
    path("standings/pl/", CurrentPLStandingsView.as_view()),
    path("scores/", ScoreListView.as_view()),
    path("update_scores/", UpdateScoresView.as_view()),
    # Pages
    path("page/pl/", pl_table),
    path("page/current/", current_standings_page),
    path("page/u/<str:username>/", user_history_page),
    path("page/home/", homepage),
    # Aggregated standings JSON
    path("standings/current/", ScoreCurrentView.as_view()),
    path("user_history/<str:username>/", UserHistoryView.as_view()),
    path("user_predictions/<str:username>/", UserPredictionsView.as_view()),
]


