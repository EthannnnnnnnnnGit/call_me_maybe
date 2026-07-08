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
	uv run python3 -m src

debug: venv
	@HF_HOME=$(HF_CACHE) \
	TRANSFORMERS_CACHE=$(HF_CACHE)/transformers \
	HF_DATASETS_CACHE=$(HF_CACHE)/datasets \
	UV_PROJECT_ENVIRONMENT=$(VENV_PATH) \
	uv run python3 -m pdb src

lint:
	uv run flake8 src
	uv run mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 src
	uv run mypy src --strict

clean:
	rm -rf */*__pycache__ */*/*__pycache__
	rm -rf .mypy_cache
	rm -rf data/output

fclean:
	rm -rf $(VENV_PATH)
	rm -rf $(HF_CACHE)
	uv clean

.PHONY: venv install run debug lint lint-strict clean fclean
