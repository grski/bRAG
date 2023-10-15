PATH  := $(PATH)
SHELL := /bin/bash

black:
	black .

ruff:
	ruff check . --fix

lint:
	make black
	make ruff

pre-commit:
	pre-commit run --all-files

test-without-clean:
	set -o pipefail; \
	pytest \
	  --color=yes \
	  --junitxml=pytest.xml \
	  --cov-report=term-missing:skip-covered \
	  --cov=app \
	  tests \
	  | tee pytest-coverage.txt

test:
	make test-without-clean
	make clean

upgrade:
	make pip-compile-upgrade
	make pip-compile-dev-upgrade


compile:
	make pip-compile
	make pip-compile-dev

sync:
	pip-sync requirements/requirements.txt
sync-dev:
	pip-sync requirements/requirements.txt requirements/requirements-dev.txt

pip-compile:
	pip-compile -o requirements/requirements.txt pyproject.toml
pip-compile-dev:
	pip-compile --extra dev -o requirements/requirements-dev.txt pyproject.toml

pip-compile-upgrade:
	pip-compile --strip-extras --upgrade -o requirements/requirements.txt pyproject.toml
pip-compile-dev-upgrade:
	pip-compile --extra dev --upgrade -o requirements/requirements-dev.txt pyproject.toml

run:
	python -m gunicorn -c settings/gunicorn.conf.py app.main:app

run-dev:
	python -m uvicorn --reload app.main:app

clean:
	rm -f pytest.xml
	rm -f pytest-coverage.txt

