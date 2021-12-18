VIRTUALENV := python3 -m venv

## help - Display help about make targets for this Makefile
help:
	@cat Makefile | grep '^## ' --color=never | cut -c4- | sed -e "`printf 's/ - /\t- /;'`" | column -s "`printf '\t'`" -t

## venv - Install the virtual environment
venv:
	$(VIRTUALENV) ~/.venv/python_project/
	ln -snf ~/.venv/python_project/ venv
	venv/bin/pip install -e '.[dev]'

## activate - Activate venv
activate:
	source venv/bin/activate

## install - Install the project locally
install: | venv

## clean - Remove the virtual environment and clear out .pyc files
clean:
	rm -rf ~/.venv/python_project/ venv
	find . -name '*.pyc' -delete
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

## lint - Lint the project
lint:
	flake8 Hector9000/*.py --count --select=E1,E2,E9,F63,F7,F82 --show-source --statistics
	#venv/bin/flake8 tests/*.py --count --select=E1,E2,E9,F63,F7,F82 --show-source --statistics

## test - Test the project
test:
	python -m pytest


.PHONY: help install clean lint test activate