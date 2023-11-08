# Flask App in Docker

- MongodDB and Heroku Deployment
- Bootstrap5 Template


## MongoDB API Key

- generate and use a MongoDB API key
- Not secure way, but replace API_KEY key in the settings.py file


## Run the Flask development server inside the container

- must provide host and port to the flask command
- by default port 5000 is used, but is not mapped to the host machine

```bash
cd app
flask --app main.py --debug run -h 0.0.0.0 -p 5555
```

- port 5555 is exposed in the Dockerfile and mapped to port 5555 on the host machine
- use brwser to access the app at [http://localhost:5555](http://localhost:5555)


