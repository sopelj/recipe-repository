# Recipe Repo

This is an attempt to rebuild my recipe site and make it open source all whilst testing out some new technologies in the process, [inertia](https://github.com/inertiajs/inertia) in this case.

> [!WARNING]
> This is **very** WIP and is just for fun.

## Features
- Create and add recipes using the Django Admin interface
- Import recipes automatically using [recipe-scrapers](https://github.com/hhursev/recipe-scrapers)
- Explore/Search recipes in Vue #TODO
- Scale and display recipes in the most appropriate units #TODO
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

1. Create virtual env
    ```bash
    python3 -m venv env
    ```
2. Activate
    ```bash
    . env/bin/activate
    ```
3. Install dependencies
    ```bash
    pip install .
    ```
4. Run migrations
    ```bash
    ./manage.py migrate
    ```
5. Create a superuser
    ```bash
    ./manage.py createsuperuser
    ```
6. Load default data
    ```bash
    ./manage.py loaddata default-units
    ```
7. Run server
    ```bash
    ./manage.py runserver
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
