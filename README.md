# 3B STORES API - TECHNIC TEST

Developed by: Octavio Gonzalez Alcala
Contact: octavio_ga@hotmail.com

## Clone the repository

``` sh
git clone https://github.com/AgedSiren557/3b-stores-api-technic-test.git
```

## How to run the project

- Install dependencies

``` sh
pip install -r requirements.txt
```

- Configure .env

```bash
  cp .env.emxample .env
```

- Run the app

``` sh
python app.py
```

## Run tests

``` sh
pytest src/test/
```

## Docker

- Build Docker Image

``` sh
docker build -t 3b-stores-api .
```

- run image (.env need to be created)

``` sh
docker run -p 5000:5000 --env-file .env 3b-stores-api
```
