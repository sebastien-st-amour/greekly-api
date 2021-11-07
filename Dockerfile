FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY greekly ./greekly
COPY migrations ./migrations
COPY config.py ./
COPY wsgi.py ./


CMD [ "python", "./wsgi.py" ]
