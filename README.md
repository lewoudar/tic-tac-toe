# Tic-tac-toe api

The goal of this project is to play with [ormar](https://collerek.github.io/ormar/) orm and fastapi. For this
purpose I decided to create an api allowing to play [tic-tac-toe](https://fr.wikipedia.org/wiki/Tic-tac-toe) game.

## Usage

You need to have [poetry](https://python-poetry.org/docs/) package manager installed. After that you can run the
following commands:

```shell
poetry install
poetry shell
alembic upgrade head
```

Then you can start an application with:

```shell
uvicorn tic_tac_toe.main:app
```

The rules of tic-tac-toe game can be easily found on the web. Here is a 
[french](https://fr.wikipedia.org/wiki/Tic-tac-toe) documentation.