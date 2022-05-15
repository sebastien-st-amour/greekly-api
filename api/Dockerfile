FROM python:3.9-slim-buster

EXPOSE 5000

WORKDIR /app

RUN apt-get update && apt-get install -y \
  vim \
  jq \
  postgresql-client \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY greekly ./greekly
COPY tests ./tests
COPY migrations ./migrations
COPY config.py ./
COPY wsgi.py ./


CMD [ "python", "./wsgi.py" ]
