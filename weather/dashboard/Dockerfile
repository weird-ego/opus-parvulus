FROM python:3.8.4-alpine3.12

COPY . /app

RUN apk update && apk upgrade && apk add --no-cache postgresql-libs \
    && apk add --no-cache --virtual .build-deps alpine-sdk postgresql-dev \
                                                libffi-dev musl-dev libffi-dev \
    && apk add libstdc++ \
    && python -mensurepip \
    && python -mpip install --user --no-cache-dir -r /app/requirements.txt \
    && apk --purge del .build-deps \
    && rm -rf /var/cache/apk/*

CMD sleep 30s && python /app/main.py
