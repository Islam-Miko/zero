FROM python:3.9.13-slim-buster as base
RUN apt-get update \
    && apt-get install -y --no-install-recommends\
    xz-utils \
    curl 
ENV POETRY_VERSION=1.1.13
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH

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
