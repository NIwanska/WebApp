# DB2 e-commerce shop project

### Setup
1. Fill .env based on .env.example.yml
2.Load variables
```
$ export $(cat .env | xargs)
```

2.Setup db in docker:
```
$ docker-compose up -d
```

3. Create venv
4. Install requirements
5. Run app
```
$ flask run
```
