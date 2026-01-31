[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/IwJY4g24)
# Bank-app

## Author:
name: Błażej

surname:Pieczulis

group:3

## How to start the app
instalacja pakietow- pip install -r requirements.txt

Odpalanie dockera do bazy- docker compose -f mongo.yml up

Odpalanie flaska- python -m flask run

## How to execute tests
wszystkie testy pytest- python -m pytest -q

behave- python -m behave

coverage- python -m coverage run --source=src -m pytest

coverage report-  python -m coverage report -m

playwright test ui- npx playwright test tests/

unit- python -m pytest tests/unit -q

api- python -m pytest tests/api -q

mongo- python -m pytest tests/integration -q
