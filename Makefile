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
	pip2 install -U -r requirements.txt
	pip2 install -U -r requirements-extras.txt

migrate:
	rm -f message.json
	python2 migrate.py

start:
	python2 challenge_server.py &
	xdg-open http://127.0.0.1:5000/

stop:
	curl -X POST http://127.0.0.1:5000/shutdown

solve: clean
	python2 solution/solution.py

solve-verbose: clean
	python2 solution/solution.py --verbose

solve-live: clean
	python2 solution/solution.py --url http://interview-challenge.manuphatak.com

solve-live-verbose: clean
	python2 solution/solution.py --url http://interview-challenge.manuphatak.com --verbose

clean:
	rm -f redis.log
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

