# Pull official base image 
FROM python:3.10-slim as base

# Set working directory
WORKDIR /app

# Set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=${PYTHONPATH}:/app

RUN apt-get update \
    && apt-get install -y gcc python3-dev build-essential libpq5

COPY poetry.lock pyproject.toml /app/

RUN pip3 install poetry
RUN poetry config virtualenvs.create false

FROM base as production
# Install dependencies
RUN poetry install --without dev
COPY . /app/
CMD ["python", "boilerplate/manage.py", "runserver"]

FROM production as development
WORKDIR /app
RUN poetry install
COPY . /app/
CMD ["python", "boilerplate/manage.py", "runserver"]