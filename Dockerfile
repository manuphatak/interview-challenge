FROM python:3.9

WORKDIR /app

# https://python-poetry.org/docs/configuration/#using-environment-variables
ENV \
  POETRY_VERSION=1.1.2 \
  POETRY_HOME="/opt/poetry" \
  POETRY_NO_INTERACTION=1 \
  FLASK_APP=challenge_server.py

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="$POETRY_HOME/bin:$POETRY_VIRTUALENVS_PATH/bin:$PATH"

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY . ./
RUN poetry run python src/migrate.py

EXPOSE 5000
ENTRYPOINT ["poetry", "run", "gunicorn", "src.wsgi:app"]

