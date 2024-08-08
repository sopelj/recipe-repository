# Recipe Repo

This is an attempt to rebuild my recipe site and make it open source all whilst testing out some new technologies in the process, [inertia](https://github.com/inertiajs/inertia) in this case.

> [!WARNING]
> This is **very** WIP and is just for fun.

## Features
- Create and add recipes using the Django Admin interface
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
3. Load default data
    ```bash
    hatch run ./manage.py loaddata admin-theme
    hatch run ./manage.py loaddata units
    hatch run ./manage.py loaddata food  # example food
    hatch run ./manage.py loaddata categories  # basic example categories
    hatch run ./manage.py loaddata qualifiers
    hatch run ./manage.py loaddata yield-units
    ```
4. Run server
    ```bash
    hatch run ./manage.py runserver
    ```

### Tests

#### Backend

```bash
hatch run test:cov
```

## Linting

```shell
pre-commit run --all-files
```

Should be running on: <http://localhost:8000/>

## Deployment

> [!WARNING]
> Not ready for production use!

Build docker image:

```bash
DOCKER_BUILDKIT=1 docker build . -f docker/Dockerfile
```
