PYTHON := python3

run:
	$(PYTHON) main.py

install:
	pip install pydantic

clean:
	rm -rf __pycache__ */*__pycache__
