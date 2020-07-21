FROM python:3.8.4-alpine3.12

COPY . /app

RUN apk update && apk upgrade && apk add --no-cache postgresql-libs \
    && apk add --no-cache --virtual .build-deps alpine-sdk postgresql-dev \
                                                libffi-dev musl-dev libffi-dev \
    && apk add libstdc++ curl \
    && python -mensurepip \
    && python -mpip install --no-cache-dir -r /app/requirements.txt \
    && apk --purge del .build-deps \
    && rm -rf /var/cache/apk/*

CMD cd /app \
    && python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py fill_cities \
    && python manage.py update_weather \
    && python manage.py create_admin \ 
    && python manage.py runserver 0:8000 
