ENV_FILE_TEST=src/.test.env
ENV_FILE=src/.env
DC=docker-compose
D=docker

up:
	${DC} --env-file ${ENV_FILE} up -d --build

down:
	${DC} --env-file ${ENV_FILE} down

mg:
	${D} --env-file ${ENV_FILE} exec -it fastapi_app bash -c "alembic upgrade head"

test:
	${DC} -f docker-compose.test.yml --env-file ${ENV_FILE_TEST} up --build -d --remove-orphans
	${DC} -f docker-compose.test.yml --env-file ${ENV_FILE_TEST} exec -it fastapi_test_app bash -c "pytest -s -vvv"
	${DC} -f docker-compose.test.yml --env-file ${ENV_FILE_TEST} down
