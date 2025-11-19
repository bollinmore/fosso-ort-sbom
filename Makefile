.PHONY: lint test all

lint:
	. .venv/bin/activate && python -m compileall -q src tests
	. .venv/bin/activate && ruff check src tests

test:
	. .venv/bin/activate && pytest

all: lint test
