SHELL := /bin/bash

# Variables definitions
# -----------------------------------------------------------------------------

ifeq ($(TIMEOUT),)
TIMEOUT := 60
endif

include .env

# Target section and Global definitions
# -----------------------------------------------------------------------------
.PHONY: all clean test install deploy down coverage gitlab docker-all docker-build docker-up docker-down docker-test black generate_dot_env

all: clean test install deploy

test:
	poetry run pytest -vv

coverage:
	poetry run pytest --cov=api --cov-report=term-missing -vv

flake8:
	poetry run flake8

requirements: poetry
	poetry export --without-hashes --format=requirements.txt > requirements.txt

poetry: generate_dot_env
	pip3 install --upgrade pip
	pip3 install poetry

install: poetry
	poetry install

superuser:
	poetry run ./manage.py createsuperuser --noinput

server:
	poetry run ./manage.py runserver_plus

shell:
	poetry run ./manage.py shell_plus

db-shell:
	poetry run ./manage.py dbshell

migrate:
	poetry run ./manage.py migrate

migrations:
	poetry run ./manage.py makemigrations

celery:
	celery -A waltzing_matilda_trading worker --loglevel=info

celery-beat:
	celery -A waltzing_matilda_trading beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler

docker-install: generate_dot_env poetry
	poetry config virtualenvs.create false
	PYTHONIOENCODING=utf8 poetry install --no-interaction

deploy: generate_dot_env docker-build
	docker-compose up -d

docker-all: docker-down docker-build docker-test docker-coverage

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down: generate_dot_env
	docker-compose down --remove-orphans

docker-test:
	docker-compose run --rm --no-deps --entrypoint="pytest -vv" api

docker-coverage:
	docker-compose run --rm --no-deps -u root --entrypoint="pytest --cov=app --cov-report=term-missing --cov-fail-under=100 -vv" api

docker-logs:
	docker-compose logs api

black:
	poetry run black -l 86 $$(find * -name '*.py')

generate_dot_env:
	@if [[ ! -e .env ]]; then \
		cp .env.example .env; \
	fi

clean:
	@find . -name '*.pyc' -exec rm -rf {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name 'Thumbs.db' -exec rm -rf {} \;
	@find . -name '*~' -exec rm -rf {} \;
	@rm -rf .cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build