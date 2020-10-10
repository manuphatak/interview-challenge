.PHONY: help setup clean start stop migrate solve solve-verbose solve-live solve-live-verbose

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

setup:
	poetry install

migrate:
	rm -f message.json
	poetry run python migrate.py

start: clean
	poetry run python challenge_server.py

stop: clean
	curl -X POST http://127.0.0.1:5000/shutdown

solve:
	poetry run python solution/solution.py

solve-verbose:
	poetry run python solution/solution.py --verbose

solve-live:
	poetry run python solution/solution.py --base http://interview-challenge.manuphatak.com

solve-live-verbose:
	poetry run python solution/solution.py --base http://interview-challenge.manuphatak.com --verbose

clean:
	rm -f challenge_server.log
	rm -rf tmp/.cache
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

