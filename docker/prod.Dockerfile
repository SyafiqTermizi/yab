FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    # translation stuff
    && apt-get install -y gettext \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY . ./

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry install --no-dev --no-root -n