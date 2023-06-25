FROM python:3.10.8

RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

WORKDIR /worker

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt


COPY . .
CMD [ "python", "worker.py"]