venv:
	source .venv/bin/activate

run:
	fastapi dev app.py

migrate:
	alembic upgrade head

revision:
ifdef name
	alembic revision --autogenerate -m $(name)
else
	echo "No revision name provided! Repeat command and add name=<revision_name>"
endif

test:
	pytest -v

coverage:
	coverage run -m pytest -v && coverage report

coverage-html:
	coverage run -m pytest -v && coverage html

# Docker
docker-run:
	docker run --rm --name boards_c -p 127.0.0.1:8080:8080 --net=host boards_i 

docker-stop:
	docker stop boards_c 

docker-build:
	docker build -t boards_i:latest .


