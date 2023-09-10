FROM python:3.10-bullseye

WORKDIR /src

COPY ./pyproject.toml ./poetry.lock /src/

RUN pip install poetry

RUN poetry install

COPY . /src/

# RUN  poetry run alembic upgrade head

# CMD ["poetry", "run", "uvicorn", "--reload", "--host=0.0.0.0", "--port=8000", "app.main:app"]