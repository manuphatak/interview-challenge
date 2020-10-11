FROM python:3.9

WORKDIR /app

# https://python-poetry.org/docs/configuration/#using-environment-variables
ENV \
  POETRY_VERSION=1.1.2 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_NO_INTERACTION=1 \
  VENV_PATH="/app/.venv"

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

COPY . .
RUN poetry install
RUN poetry run migrate


ENV FLASK_APP=challenge_server.py
EXPOSE 5000
# ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
ENTRYPOINT ["poetry", "run", "gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "src.wsgi:app"]


