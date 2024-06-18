# Recipe Repo

This is an attempt to rebuild my recipe site and make it open source all whilst testing out some new technologies in the process, [intertia](https://github.com/inertiajs/inertia) in this case.

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
    pip install -r requirements.txt
    ```
4. Run migrations
    ```shell
    ./manage.py migrate
    ```
5. Run server
    ```shell
    ./manage.py runserver
    ```

Should be running on: <http://localhost:8000/>
