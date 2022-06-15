
FROM ubuntu:20.04


EXPOSE 5000

WORKDIR /app

RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y \
  vim \
  python3.9 \
  python3-pip \
  jq \
  postgresql-client \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python3.9 -m pip install -r requirements.txt

COPY greekly ./greekly
COPY tests ./tests
COPY migrations ./migrations
COPY config.py ./
COPY wsgi.py ./


CMD [ "python3.9", "./wsgi.py" ]
