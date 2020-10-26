.PHONY: help setup clean start stop migrate solve solve-verbose solve-live solve-live-verbose development-build development-up production-build production-up

help:
	@echo "setup                pip install requirements"
	@echo "migrate              create mock database"
	@echo "start                start local server as background process"
	@echo "stop                 shutdown local server"
	@echo "solve                demonstrate solution"
	@echo "solve-verbose        demonstrate solution with detailed output"
	@echo "solve-live           demonstrate solution on a live server"
	@echo "solve-live-verbose   demonstrate solution on a live server with detailed output"
	@echo "clean                remove file artifacts"
	@echo "development-build    build docker compose"
	@echo "development-up       serve docker compose"
	@echo "production-build     build docker compose"
	@echo "production-up        serve docker compose"

setup:
	poetry install

migrate:
	rm -f message.json
	poetry run python src/migrate.py

start: clean
	poetry run python src/challenge_server.py

stop: clean
	curl -X POST http://127.0.0.1:5000/shutdown

solve:
	poetry run python src/solution/solution.py

solve-verbose:
	poetry run python src/solution/solution.py --verbose

solve-live:
	poetry run python src/solution/solution.py --base http://interview-challenge.manuphatak.com

solve-live-verbose:
	poetry run python src/solution/solution.py --base http://interview-challenge.manuphatak.com --verbose

clean:
	rm -rf tmp
	find . -name '*.log' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

development-build:
	docker-compose -f docker-compose.yml -f docker-compose.development.yml build

development-up:
	docker-compose -f docker-compose.yml -f docker-compose.development.yml up

production-build:
	docker-compose -f docker-compose.yml -f docker-compose.production.yml build

production-up:
	docker-compose -f docker-compose.yml -f docker-compose.production.yml up

