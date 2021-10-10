FROM python:3.8-alpine3.13 AS builder
WORKDIR /app
COPY . /app
RUN apk update
RUN apk add build-base postgresql-dev gcc python3-dev musl-dev make libffi-dev openssl-dev cargo
RUN pip install pipenv

FROM builder AS development
RUN pipenv install --dev
EXPOSE 4444

FROM builder AS production
RUN pipenv install
CMD ["pipenv", "run", "gunicorn", "-c", "gunicorn.conf.py", "app.main:app"]
