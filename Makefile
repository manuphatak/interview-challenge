.PHONY: help setup clean start stop migrate solve solve-clean

help:
	@echo "setup - use pip to install requirements"
	@echo "migrate - migrate message database"
	@echo "start - start local server to host challenge"
	@echo "stop - shutdown local server"
	@echo "solve - demonstrate solution"
	@echo "solve-clean - clear the cache and demonstrate solution"
	@echo "clean - remove cache and Python file artifacts"

setup:
	pip2install -r requirements.txt
	pip2 install -r requirements-extras.txt

migrate:
	rm -f message.json
	python2 migrate.py

start:
	python2 challenge_server.py &
	xdg-open http://127.0.0.1:5000/

stop:
	curl -X POST http://127.0.0.1:5000/shutdown

server: start

solve:
	python2 solution/solution.py

solve-clean: clean solve

clean:
	rm -f cache.json
	rm -f redis.log
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

