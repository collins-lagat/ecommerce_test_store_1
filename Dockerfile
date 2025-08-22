FROM python:3.12.4-slim-bookworm

# Set the default config file
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/home/app/.local/bin:$PATH
ARG GROUP_ID=1000
ARG USER_ID=1000

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# Install base dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  vim \
  # To install psycopg2
  libpq-dev libpq5 \
  # To install python-ldap
  libldap2-dev libsasl2-dev slapd ldap-utils tox lcov valgrind \
  && rm -rf /var/lib/apt/lists/*

# Create a group and user
RUN groupadd -g ${GROUP_ID} app \
  && useradd -m -l -u ${USER_ID} -g app app \
  && mkdir -p /app /app/static /app/media /home/app/.local/bin /home/app/.local/lib \
  && chown -R app:app /app /app/static /app/media /home/app/.local /home/app/.local/bin /home/app/.local/lib

USER app

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt


