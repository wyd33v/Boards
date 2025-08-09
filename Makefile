venv:
	source .venv/bin/activate

run:
	python main.py

migrate:
	alembic upgrade head

revision:
ifdef name
	alembic revision --autogenerate -m $(name)
else
	@echo "No revision name provided! Repeat command and add name=<revision_name>"
endif
