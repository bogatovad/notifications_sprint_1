FROM python:3.10.8-bullseye

WORKDIR /admin
RUN mkdir -p /admin/static/ \
    && mkdir -p /admin/media/ \
    && groupadd -r usr \
    && useradd -d /admin/ -r -g usr usr \
    && chown usr:usr -R /admin/

COPY requirements.txt requirements.txt
COPY wait-for-it.sh /admin/
RUN chmod +x ./wait-for-it.sh
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    # https://stackoverflow.com/questions/46711990/error-pg-config-executable-not-found-when-installing-psycopg2-on-alpine-in-dock \
     # https://stackoverflow.com/a/67404591
     apt-get -y install libpq-dev gcc

USER usr
COPY . .
EXPOSE 8000
# https://medium.com/@krishnaregmi/wait-for-it-docker-compose-f0bac30f3357
CMD ./wait-for-it.sh ${DB_HOST}:${DB_PORT} \
    && python manage.py collectstatic --noinput \
    && python manage.py migrate \
    && gunicorn config.wsgi --bind 0.0.0.0:8000 --reload