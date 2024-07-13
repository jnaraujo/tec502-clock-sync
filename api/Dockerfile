FROM python:3.12.3

WORKDIR /app

ENV POETRY_VERSION=1.8.3

RUN pip install poetry==$POETRY_VERSION
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install

COPY . /app

WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]