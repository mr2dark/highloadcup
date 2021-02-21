FROM python:latest

RUN apt-get update --fix-missing -y \
    && apt-get install -y --no-install-recommends \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt requirements.txt
RUN pip install -U -r requirements.txt

COPY . /app
WORKDIR /app
ENTRYPOINT ["python", "main.py"]
