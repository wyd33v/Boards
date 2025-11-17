venv:
	source .venv/bin/activate

run:
	fastapi dev app.py

migrate:
	alembic -c ./data/alembic.ini upgrade head

revision:
ifdef name
	alembic -c ./data/alembic.ini revision --autogenerate -m $(name)
else
	echo "No revision name provided! Repeat command and add name=<revision_name>"
endif

test:
	pytest -v

coverage:
	coverage run -m pytest -v && coverage report

coverage-html:
	coverage run -m pytest -v && coverage html


#cleanning

pyclean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

black-clean:
	black .

ruff-fix:
	ruff check . --fix

isort-fix:
	isort .

bandit:
	bandit -r .

lint:
	ruff check .
	mypy .

precommit-clean:
	pre-commit clean

precommit-install:
	pre-commit install

precommit-run-all:
	pre-commit run --all-files

precommit-update:
	pre-commit autoupdate
# Docker
docker-run:
	docker run --rm --name boards_c -p 127.0.0.1:8080:8080 --net=host boards_i

docker-stop:
	docker stop boards_c

docker-build:
	docker build -t boards_i:latest .

docker-up:
	docker-compose up

docker-down:
	docker-compose down --remove-orphans

up-cache:
	docker-compose up cache
