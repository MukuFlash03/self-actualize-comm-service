FROM python:3.10-alpine3.20

ENV DATABASE_URL="sqlite:///test.db"

ENV PYTHONUNBUFFERED=1

WORKDIR /app/communication-microservice

RUN apk add --no-cache bash

COPY . .

RUN pip3 install -r requirements.txt

# CMD ["python", "main.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app", "--log-level", "info"]
