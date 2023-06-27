FROM python:3.10.8

RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

WORKDIR /notification_service
ENV PYTHONPATH=$PYTHONPATH:$ROOT_DIR/src

RUN groupadd -r notification_service && useradd -d /notification_service -r -g notification_service notification_service

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY src/ /notification_service
COPY wait_for.sh /notification_service
RUN chown notification_service:notification_service -R /notification_service
RUN chmod +x wait_for.sh

USER notification_service

CMD ./wait_for.sh rabbitmq:5672 && gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8080
