FROM python:3.9-slim-buster

EXPOSE 5000

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY greekly ./greekly
COPY tests ./tests
COPY migrations ./migrations
COPY config.py ./
COPY wsgi.py ./


CMD [ "python", "./wsgi.py" ]
