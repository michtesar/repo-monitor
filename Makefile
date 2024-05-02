.DEFAULT_GOAL := all

source = repo_monitor/ tests/

.PHONY: .pdm
.pdm:
	@pdm -V || echo 'Please install PDM: https://pdm.fming.dev/latest/#installation'

.PHONY: .mypy
.mypy:
	@mypy -V || echo 'Please install Mypy: https://mypy.readthedocs.io/en/stable/getting_started.html'

.PHONY: .pre-commit
.pre-commit:
	@pre-commit -V || echo 'Please install pre-commit: https://pre-commit.com/'

.PHONY: install  ## Auto-format python source files
install: .pdm .pre-commit
	pdm info
	pdm install --group :all
	pdm run pre-commit install --install-hooks

.PHONY: lint  ## Lint Python source files
lint: .pdm
	pdm run ruff check $(sources)
	pdm run ruff format --check$(sources)

.PHONY: codespell  ## Use Codespell to perform spellchecking
codespell: .pdm
	pdm run codespell --all-files

.PHONY: typecheck  ## Use Mypy to perform type checking
typecheck: .mypy
	pdm run mypy $(sources)

.PHONY: test  ## Run all tests
test: .pdm
	pdm run pytest tests

.PHONY: clean  ## Clear local caches and build artifacts
clean:
	rm -rf `find . -name __pycache__`
	rm -rf `find . -type '*.py[co]'`
	rm -rf `find . -type '*~'`
	rm -rf `find . -type '.*~'`
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist

.PHONY: run  ## Run the application
run:
	pdm run uvicorn repo_monitor.main:app

.PHONY: dependencies  ## Export all prod dependencies to requirements.txt
dependencies:
	pdm export --production -o requirements.txt

.PHONY: all
all: clean install format test run

.PHONY: help  ## Display help
help:
	@grep -E \
		'^.PHONY: .*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ".PHONY: |## "}; {printf "\033[36m%-19s\033[0m %s\n", $$2, $$3}'
