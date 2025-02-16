ENV_FILE=src/.env

up:
	docker-compose --env-file ${ENV_FILE} up -d --build

down:
	docker-compose --env-file ${ENV_FILE} down

test_up:
	docker-compose -f docker-compose.test.yml --env-file src/.env.test up -d

test_down:
	docker-compose -f docker-compose.test.yml --env-file src/.env.test down