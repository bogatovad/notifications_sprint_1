FROM python:3.10.8

RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

ARG ROOT_DIR=/notification_service
WORKDIR $ROOT_DIR
ENV PYTHONPATH=$PYTHONPATH:$ROOT_DIR/src

RUN groupadd -r notification_service && useradd -d $ROOT_DIR -r -g notification_service notification_service

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY src/ $ROOT_DIR
COPY entrypoint.sh $ROOT_DIR
RUN chown notification_service:notification_service -R $ROOT_DIR
RUN chmod +x entrypoint.sh

USER notification_service

#ENTRYPOINT ["sh", "entrypoint.sh", ]
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080"]
