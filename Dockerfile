FROM python:3.9.13-buster as base

#ENV PYTHONDONTWRITEBYTECODE=1 \ 
#   PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.1.13
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH /root/.poetry/bin:$PATH

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN python -m venv --copies /app/venv
RUN . /app/venv/bin/activate && poetry install

FROM python:3.9.13-slim-buster as prod

COPY --from=base /app/venv /app/venv/
ENV PATH /app/venv/bin:$PATH

WORKDIR /app
COPY . ./

CMD ["bash", "start-api.sh"]
