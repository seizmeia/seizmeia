all: run

run: run.local ## Runs the service locally
run.local:
	@python -m seizmeia

bup: ## Start development environment services
	@docker compose up --build --detach

down: ## Stop development environment services
	@docker compose down --remove-orphans

log: logs ## Shows container logs
logs:
	@docker compose logs -f seizmeia

format: ## Formats code
	@python -m isort .
	@python -m black .

test: typecheck unittest ## Tests code for typecheck and unit tests

typecheck: ## Type checks source code
	@mypy seizmeia

unittest: ## Runs unit tests
	@pytest

coverage: ## Gets code test coverage
	@coverage erase
	@coverage run -m pytest 1> /dev/null
	@coverage report

ci:
	@tox

env:
	@tox -e python3.10 --devenv .venv

pre-commit:
	@pre-commit run --all-files

.PHONY: web web.dev
web:
	npm --prefix web run build
web.dev:
	npm --prefix web run dev

clear: clean ## Clears the repository
clean:
	@rm -rf **/__pycache__ .mypy_cache .pytest_cache .vscode .coverage *.egg-info .tox .venv *.db

help: ## Show this help
	@printf "\033[32m\xE2\x9c\x93 usage: make [target]\n\033[0m"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
