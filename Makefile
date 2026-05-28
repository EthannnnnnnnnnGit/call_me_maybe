PROJECT_NAME = CallMeMaybe
VENV_PATH = /tmp/$(PROJECT_NAME)-venv
HF_CACHE = /tmp/$(PROJECT_NAME)-hf

install:
	UV_PROJECT_ENVIRONMENT=$(VENV_PATH) uv sync
	ln -sfn $(VENV_PATH) .venv

run: venv
	@HF_HOME=$(HF_CACHE) \
	TRANSFORMERS_CACHE=$(HF_CACHE)/transformers \
	HF_DATASETS_CACHE=$(HF_CACHE)/datasets \
	UV_PROJECT_ENVIRONMENT=$(VENV_PATH) \
	uv run python3 -m srcs

debug: venv
	@HF_HOME=$(HF_CACHE) \
	TRANSFORMERS_CACHE=$(HF_CACHE)/transformers \
	HF_DATASETS_CACHE=$(HF_CACHE)/datasets \
	UV_PROJECT_ENVIRONMENT=$(VENV_PATH) \
	uv run python3 -m pdb srcs

lint:
	flake8 srcs
	mypy srcs --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 srcs
	mypy srcs --strict

clean:
	rm -rf */*__pycache__ */*/*__pycache__
	rm -rf .mypy_cache

.PHONY: venv
