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


## Arch
![image](https://user-images.githubusercontent.com/54863119/142964366-adf7e54c-8794-47e5-b66f-6c0bbaaff074.png)
