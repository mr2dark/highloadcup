FROM python:3.8-slim

RUN apt-get update --fix-missing -y \
    && apt-get install -y --no-install-recommends \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8000

CMD gunicorn --worker-class gevent \
  --workers 1 \
  --worker-connections 1000 \
  --bind 0.0.0.0:8000 \
  openapi_server:app

HEALTHCHECK --interval=5s --timeout=3s --start-period=15s \
  CMD curl -f http://localhost:8000/health-check || exit 1