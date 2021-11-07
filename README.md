# Greekly API

## Create Migration Repository (only run once)
```
flask db init
```

## Run Migrations
```
flask db migrate -m "Initial migration."
flask db upgrade
```

## Run app
```
python wsgi.py
```