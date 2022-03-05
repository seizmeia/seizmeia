all: run

run: run.uvicorn
run.local:
	@python -m seizmeia:__main__
run.uvicorn:
	@uvicorn seizmeia.server:app --reload

bup: ## Start development environment services
	@docker compose up --build --detach

down: ## Stop development environment services
	@docker compose down --remove-orphans

log: logs ## Shows container logs
logs:
	@docker compose logs -f seizmeia

format: ## Formats code
	@isort seizmeia/**.py tests/**.py
	@black seizmeia tests --line-length 79

test: typecheck unittest ## Tests code for typecheck and unit tests

typecheck: ## Type checks source code
	@mypy seizmeia

unittest: ## Runs unit tests
	@pytest tests --asyncio-mode=strict

coverage: ## Gets code test coverage
	@coverage run -m --source=seizmeia pytest tests 1> /dev/null
	@coverage report

ci:
	@tox

clear: clean ## Clears the repository
clean:
	@rm -rf **/__pycache__ .mypy_cache .pytest_cache .vscode .coverage *.egg-info .tox

help: ## Show this help
	@printf "\033[32m\xE2\x9c\x93 usage: make [target]\n\033[0m"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
