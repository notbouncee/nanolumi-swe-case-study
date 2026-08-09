.PHONY: format test run install

install:
	pip install -e .[dev]

format:
	black src/ tests/ scripts/

test:
	PYTHONPATH=. pytest tests/ --ignore=tests/e2e/

teste2e:
	PYTHONPATH=. pytest tests/e2e/

run:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
