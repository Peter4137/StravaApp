FROM python:3.11.0a6-slim-buster as base

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev

RUN pip3 install 'poetry==1.1.11' \
    && poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./


FROM base as production
RUN poetry install --no-dev
COPY todo_app todo_app

ENTRYPOINT poetry run gunicorn todo_app.wsgi:start -b 0.0.0.0:80

FROM base as development
RUN poetry install
COPY todo_app todo_app

ENTRYPOINT poetry run flask run --host=0.0.0.0 --port=5000

FROM base as test_unit_integration
RUN poetry install

COPY todo_app todo_app
COPY test test
COPY .env.test ./
ENTRYPOINT [ "poetry", "run", "pytest", "./test/tests" ]

FROM base as test_e2e
RUN poetry install

RUN apt-get install -y firefox-esr curl
ENV GECKODRIVER_VER v0.30.0
RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/ \
   && rm geckodriver-*.tar.gz

COPY todo_app todo_app
COPY test test
ENTRYPOINT [ "poetry", "run", "pytest", "./test/e2e_tests" ]



