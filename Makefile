start:
	docker compose up

start-build:
	docker compose up --build

lint:
	pip install auth && \
	pip install auth/.[lint] && \
	mypy auth && mypy app && mypy rag

stop:
	docker compose stop

envs:
	source ./.profile