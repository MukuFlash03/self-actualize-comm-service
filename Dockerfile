FROM python:3.10-alpine3.20

ENV PYTHONUNBUFFERED=1

WORKDIR /app/communication-microservice

RUN apk add --no-cache bash

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python", "main.py"]
