FROM python:3.12-alpine AS build-image

RUN apk add postgresql-dev build-base python3-dev jpeg-dev zlib-dev openldap-dev
RUN python -m venv /opt/venv

WORKDIR /opt/
ADD ./pyproject.toml /opt/pyproject.toml
RUN set -ex \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -e .[test,ldap,production]


FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG GID=1000
ARG UID=1000

# Create the app user
RUN set -ex \
    && addgroup -S django --gid "${GID}" \
    && adduser -S django --uid "${UID}" -G django

COPY --from=build-image /opt/venv /opt/venv

# Install Deps (translations and SSR)
RUN apk add --no-cache bash nodejs yarn gettext libpq-dev libldap


# Entrypoint
COPY ./docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Dev command wrapper
COPY ./docker/run-dev-servers.sh /run-dev-servers.sh
RUN chmod +x /run-dev-servers.sh

ENV PATH=/opt/venv/bin:$PATH

# Set DB variables in default shell so docker exec -it will have it
ENV ENV=/home/django/.ashrc
RUN echo 'export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_DB_HOST}/${POSTGRES_DB}"' > "$ENV"

WORKDIR /app

EXPOSE 8000
USER django

ENTRYPOINT ["/entrypoint.sh"]
