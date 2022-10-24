# getting started

## initial setup

```bash
cd Backend
python3 -m venv venv
```

## install dependencies

```bash
pip install -r requirements.txt
```

## Set up the Database

With Postgres running, create a `wallet` database:

```bash
createbd wallet
createdb wallet_test
```

## Run the Server

From within the `./backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
FLASK_DEBUG=true flask run --reload
```

## Testing

Ensure to Write at least one test for the success and at least one error behavior for each endpoint you create using the unittest library.

To deploy the tests, run

```bash
python3 test_flaskr.py
```
