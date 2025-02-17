ENV_FILE=src/.env
DC=docker-compose

up:
	${DC} --env-file ${ENV_FILE} up -d --build

down:
	${DC} --env-file ${ENV_FILE} down

test_up:
	${DC} -f docker-compose.test.yml --env-file src/.env.test up -d

test_down:
	${DC} -f docker-compose.test.yml --env-file src/.env.test down

test_go:
	python3 -m pytest tests/ -s -v

mg:
	alembic upgrade head