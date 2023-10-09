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
	poetry run pytest \
	  --color=yes \
	  --junitxml=pytest.xml \
	  --cov-report=term-missing:skip-covered \
	  --cov=app \
	  tests \
	  | tee pytest-coverage.txt

test:
	make test-without-clean
	make clean

run:
	python -m gunicorn -c settings/gunicorn.conf.py app.main:app

run-dev:
	python -m uvicorn --reload app.main:app

clean:
	rm -f pytest.xml
	rm -f pytest-coverage.txt

