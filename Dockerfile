FROM python:3.10

WORKDIR /code
COPY poetry.lock pyproject.toml ./
RUN pip install --upgrade pip && pip install poetry && poetry install --no-dev
COPY . .

