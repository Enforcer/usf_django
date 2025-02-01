.PHONY: init
init:
	uv sync

.PHONY: fmt
fmt:
	uv run ruff format

.PHONY: lint
lint:
	uv run ruff check --fix
	PYTHONPATH=usf uv run mypy usf/ tests/
	uv run lint-imports
	# For faster feedback locally use mypy like:
	# PYTHONPATH=usf uv run dmypy run --timeout 3600 -- tests/ usf/

.PHONY: test
test:
	uv run pytest tests/

.PHONY: all
all: fmt lint test

.PHONY: run
run:
	uv run usf/manage.py runserver 0.0.0.0:8000

.PHONY: migrate
migrate:
	uv run usf/manage.py migrate

