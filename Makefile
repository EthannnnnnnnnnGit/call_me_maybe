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

clean:
	rm -rf */*__pycache__ */*/*__pycache__

.PHONY: venv
