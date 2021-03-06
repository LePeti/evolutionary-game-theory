.PHONY: help test clean main ipython

.DEFAULT: help

help:
	@echo "make test"
	@echo "       clean"
	@echo "       run tests"
	@echo "make clean"
	@echo "       clean up .pyc files"
	@echo "make main"
	@echo "       clean"
	@echo "       run main.py"
	@echo "make ipython"
	@echo "       open ipython3"

test: clean
	@pipenv run python -m unittest discover -s tests $(TESTARGS)

clean:
	@find . -name '*.pyc' -delete

main: clean
	@pipenv run python main.py

ipython:
	@pipenv run ipython3