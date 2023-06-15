BASE_COMMAND = docker-compose run --rm ${SERVICE_NAME}
COMMAND = ${BASE_COMMAND}  /bin/bash -c
COMPOSE = docker-compose
MANAGE_PY = python3 manage.py

build:
	${COMPOSE} build

start:
	${COMPOSE} start

stop:
	${COMPOSE} stop

up:
	${COMPOSE} up

bash:
	docker-compose run --rm admin /bin/bash

down:
	${COMPOSE} down

BASE_COMMAND = docker-compose -f ${COMPOSE_FILE} run --rm django
COMMAND = ${BASE_COMMAND}  /bin/bash -c

superuser:
	docker-compose run --rm admin /bin/bash -c './manage.py createsuperuser'

shell:
	docker-compose run --rm admin /bin/bash -c  './manage.py shell'