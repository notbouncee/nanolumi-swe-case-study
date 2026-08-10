.PHONY: test-backend test-backend-e2e test-frontend test-all

# Backend tests
test-backend:
	@echo "Running backend unit tests in Docker..."
	docker compose exec -T -e PYTHONPATH=/app backend pytest tests/ --ignore=tests/e2e/

test-backend-e2e:
	@echo "Running backend E2E tests in Docker..."
	docker compose exec -T -e PYTHONPATH=/app backend pytest tests/e2e/

# Frontend E2E tests using Playwright
test-frontend:
	@echo "Running frontend Playwright tests..."
	cd frontend && npm run test:e2e

# Run all tests sequentially
test-all: test-backend test-backend-e2e test-frontend
	@echo "All tests completed successfully!"
