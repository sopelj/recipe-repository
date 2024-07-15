# Recipe Repo

This is an attempt to rebuild my recipe site and make it open source all whilst testing out some new technologies in the process, [inertia](https://github.com/inertiajs/inertia) in this case.

> [!WARNING]
> This is **very** WIP and is just for fun.

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

## Frontend

1. Install packages
    ```shell
    yarn
    ```
2. Start dev server
    ```shell
    yarn dev
    ```

## Backend

1. Create virtualenv
    ```shell
    python3 -m venv env
    ```
2. Activate
    ```shell
    . env/bin/activate
    ```
3. Install dependencies
    ```shell
    pip install .
    ```
4. Run migrations
    ```shell
    ./manage.py migrate
    ```
5. Create a super user
    ```shell
    ./manage.py createsuperuser
    ```
6. Load default data
    ```shell
    ./manage.py loaddata default-units
    ```
7. Run server
    ```shell
    ./manage.py runserver
    ```

Should be running on: <http://localhost:8000/>
