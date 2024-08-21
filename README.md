# Recipe Repository

A repository for all your recipes. Put all your saved recipes in one location and share them with family and friends.

> [!WARNING]
> This still a WIP and is mostly just for fun.

## Features
- Add and manage recipes using the Django Admin interface
- Import recipes automatically using [recipe-scrapers](https://github.com/hhursev/recipe-scrapers)
- Explore/Search recipes
- Scale and display recipes in the most appropriate units
- Convert between Metric and Imperial Units #TODO

## Why another recipe manager site?

A lot of other projects already exist that fulfill most needs.

I really hesitated about using one of them, but there were a few things I really wanted, mainly:
   - Share any recipe without expiration dates
   - Scaling units dynamically and switching to the most appropriate units
   - Switching between metric and imperial on any recipe
   - Multilingual recipes

I wasn't able to find one project that did all of that currently, but, really, mainly I just wanted to work on a project for fun, and if it can be useful to others all the better.

## Development

### Dependencies
 - Python (3.12+)
 - Yarn + Node (v20+)

### Env

Copy example env file and make changes as required.
Notably, change the `DJANGO_SECRET`.

```shell
cp example.env .env
```

### Frontend

1. Install packages
    ```bash
    yarn
    ```
2. Start dev server
    ```bash
    yarn dev
    ```

### Backend

> [!NOTE]
> These examples all use [`hatch`](https://hatch.pypa.io/latest/),
> but you can also create your on venv, install dependencies, and run ./manage.py directly

1. Run migrations
    ```bash
    hatch run ./manage.py migrate
    ```
2. Create a superuser
    ```bash
    hatch run ./manage.py createsuperuser
    ```
3. Compile Translations
    ```bash
    hatch run ./manage.py compilemessages
    ```
4. Load default data
    ```bash
    hatch run ./manage.py loaddata admin-theme
    hatch run ./manage.py loaddata units
    hatch run ./manage.py loaddata food  # example food
    hatch run ./manage.py loaddata categories  # basic example categories
    hatch run ./manage.py loaddata qualifiers
    hatch run ./manage.py loaddata yield-units
    ```
5. Run server
    ```bash
    hatch run ./manage.py runserver
    ```

### Tests

#### Backend

```bash
hatch run test:cov
```

#### Frontend

```bash
yarn test
```

## Linting

```shell
pre-commit run --all-files
```

Should be running on: <http://localhost:8000/>

## Deployment

> [!WARNING]
> PoC. Not ready for production use.

### Settings

Settings can be configured via environment variables

| Setting                 | Default                  | Note                                                                   |
|-------------------------|--------------------------|------------------------------------------------------------------------|
| `SECRET_KEY`            | `None` *Required*        | Must be set to a secure random string                                  |
| `DEBUG`                 | `False`                  | Enable Django debug mode (Don't use in production)                     |
| `QUERY_LOGGING_ENABLED` | `False`                  | Log all DB queries for debugging purposes                              |
| `WERKZEUG_DEBUG_PIN`    | `None`                   | Werkzeug PIN (can be set to `off` to diable. Only do this locally! )   |
| `SSL_ENABLED`           | `False`                  | Use HTTPS in Django. Set to True when Django is behind HTTPS proxy     |
| `POSTGRES_DB`           | `"recipe_repo"`          | Postgres Database Table Name                                           |
| `POSTGRES_USER`         | `"recipe_repo"`          | Postgres Database User                                                 |
| `POSTGRES_PASSWORD`     | `"insecure-change-this"` | Postgres Database Password - Set to something secure if using Postgres |
| `POSTGRES_HOST`         | `"db"`                   | Postgres Database Host                                                 |
| `MEMCACHED_ENABLED`     | `False`                  | Enable Memcached                                                       |
| `MEMCACHED_HOST`        | `None`                   | Memcached connection string. ex. "pymemcache://memcached:11211"        |
| `AUTH_LDAP_ENABLED`     | `False`                  | Enable LDAP Authentication                                             |
| `VITE_APP_THEME_COLOUR` | `"#482880"`              | Primary theme colour                                                   |
| `VITE_APP_TITLE`        | `"Recipe Repository"`    | Main site title                                                        |
| `VITE_APP_TITLE_SHORT`  | `"Recipes"`              | Short title for web app                                                |

### Docker

Build docker image:

```bash
DOCKER_BUILDKIT=1 docker build . -f docker/Dockerfile
```
