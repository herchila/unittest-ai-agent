.PHONY: install dev test lint format clean build help

# Variables
POETRY = poetry
PYTHON_DIRS = "ut example"

help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

lock:
	$(POETRY) lock

install:
	$(POETRY) install --only=main

dev:
	$(POETRY) install --only=dev

test:
	$(POETRY) run pytest -s -v

test-cov:
	$(POETRY) run pytest -s --cov=ut --cov-report= --cov-branch -v

format: ## Format code
	$(POETRY) run black $(PYTHON_DIRS)
	$(POETRY) run isort $(PYTHON_DIRS)
	@echo "✅ code formatted"

pre-commit: ## Run pre-commit hooks
	$(POETRY) run pre-commit run --all-files

check: pre-commit test  ## Run all checks

clean: ## Clean temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -name ".coverage" -delete
	find . -name "htmlcov" -exec rm -rf {} +
	find . -name ".pytest_cache" -exec rm -rf {} +
	find . -name ".mypy_cache" -exec rm -rf {} +
	@echo "✅ Temp files removed"

info:
	$(POETRY) show
	$(POETRY) run ut --version

deps-update:
	$(POETRY) update

deps-show:
	$(POETRY) show --tree

verify: ## Verify environment and tools
	@echo "🔍 Verifying tools..."
	@$(POETRY) run python --version || echo "❌ Python not available"
	@$(POETRY) run pytest --version || echo "❌ pytest not installed"
	@echo "✅ Verification complete"
