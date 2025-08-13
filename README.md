# prediction-league
English Premier League prediction tool
Setup
1) Create venv and install deps
   - python3 -m venv .venv
   - .venv/bin/python -m pip install -U pip setuptools wheel
   - .venv/bin/python -m pip install django djangorestframework requests

2) Run Django
   - .venv/bin/python manage.py migrate
   - .venv/bin/python manage.py runserver

Management commands
   - .venv/bin/python manage.py init_teams
   - .venv/bin/python manage.py init_gameweeks
   - .venv/bin/python manage.py init_predictions /path/to/predictions.csv --season "2025/26"
   - .venv/bin/python manage.py update_scores --season "2025/26"