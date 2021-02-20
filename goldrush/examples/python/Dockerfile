FROM python:latest

COPY ./requirements.txt requirements.txt
RUN pip install -U -r requirements.txt

COPY . /app
WORKDIR /app
ENTRYPOINT ["python", "main.py"]
