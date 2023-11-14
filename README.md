# Flask App in Docker

- MongodDB and Heroku Deployment
- Bootstrap5 Template


## MongoDB API Key

- generate and use a MongoDB API key
- Not secure way, but replace API_KEY key in the settings.py file


## Run the Flask development server inside the container

- must provide host and port to the flask command
- by default port 5000 is used, but is not mapped to the host machine
- use gunicorn to run the app in production or locally with port 5555
```bash
cd app
flask --app app.main.py --debug run -h 0.0.0.0 -p 5555
gunicorn --workers=2 app.main:app -b 0.0.0.0:5555
```

- port 5555 is exposed in the Dockerfile and mapped to port 5555 on the host machine
- use brwser to access the app at [http://localhost:5555](http://localhost:5555)

## Deploy App to Heroku

- create your free account on [Heroku](https://www.heroku.com/)
- install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- Heroku CLI is already installed in this Docker image
- login to Heroku
```bash
heroku login
```
- create a new app
```bash
heroku create -a flask-app-docker
```
- push the app to Heroku
```bash
git push heroku main
```
- open the app in the browser
```bash
heroku open
```
- check the logs
```bash
heroku logs --tail
