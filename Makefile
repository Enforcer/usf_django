.PHONY: init
init:
	uv sync

.PHONY: fmt
fmt:
	uv run ruff format

.PHONY: lint
lint:
	uv run ruff check --fix
	uv run dmypy run --timeout 3600 -- tests/ usf/
	uv run lint-imports

.PHONY: qa
qa: fmt lint

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

