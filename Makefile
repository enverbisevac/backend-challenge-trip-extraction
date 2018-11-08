.PHONY: help install test lint run doc

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

.DEFAULT: help
help:
	@echo "make install"
	@echo "       prepare development environment, use only once"
	@echo "make test"
	@echo "       run tests"
	@echo "make lint"
	@echo "       run pylint and mypy"
	@echo "make run"
	@echo "       run project"
	@echo "make doc"
	@echo "       build sphinx documentation"

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate:
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -r requirements.txt
	touch $(VENV_NAME)/bin/activate

install:
	rm -rf venv
	make venv

test: venv
	${PYTHON} -m pytest

lint: venv
	${PYTHON} -m pylint main.py processor.py utils.py settings.py \
				main_test.py processor_test.py utils_test.py
	${PYTHON} -m mypy main.py processor.py utils.py \
				main_test.py processor_test.py utils_test.py

run: venv
	${PYTHON} main.py

doc: venv
	$(VENV_ACTIVATE) &amp;&amp; cd docs; make html