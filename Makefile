ENV_FILE=src/.env

up:
	docker-compose --env-file ${ENV_FILE} up -d --build

down:
	docker-compose --env-file ${ENV_FILE} down