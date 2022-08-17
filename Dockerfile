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

FROM base as prod-venv
RUN python -m venv --copies /venv
RUN . /venv/bin/activate && poetry install --no-dev

FROM base as test
RUN python -m venv --copies /venv
RUN . /venv/bin/activate && poetry install
COPY . ./
ENV PATH /venv/bin:$PATH
CMD ["pytest", "."]


FROM python:3.9.13-slim-buster as prod
COPY --from=prod-venv /venv /venv/
ENV PATH /venv/bin:$PATH
COPY . ./
CMD ["bash", "start-api.sh"]
