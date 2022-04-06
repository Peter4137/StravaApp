FROM python:3.11.0a6-slim-buster as base

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev

RUN pip3 install 'poetry==1.1.11' \
    && poetry config virtualenvs.create false

WORKDIR /todo-app
COPY poetry.lock poetry.toml pyproject.toml ./

FROM base as production
RUN poetry lock
RUN poetry install --no-dev
COPY todo_app todo_app
WORKDIR /todo-app/todo_app

ENTRYPOINT poetry run gunicorn wsgi:start -b 0.0.0.0:80

FROM base as development
RUN poetry lock
RUN poetry install

ENTRYPOINT poetry run flask run --host=0.0.0.0


