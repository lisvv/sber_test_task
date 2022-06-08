SHELL := /bin/bash
pip: ## install deps
	if [ ! -d ./venv ]; then \
		python3 -m venv venv; \
	fi
	source venv/bin/activate &&	pip install -r requirements.txt

clean: ## remove python/pytest cache files and other temp junk
	find . -name '*.pyc' | xargs rm -rf
	find . -name '*__pycache__' | xargs rm -rf
	find . -name '*.cache' | xargs rm -rf
	rm -r .mypy_cache 2>/dev/null || true
	rm -r .pytest_cache 2>/dev/null || true
	rm -r htmlcov 2>/dev/null || true
	rm -r .coverage 2>/dev/null || true

autoflake: ## check for unused variables and imports
	./lint autoflake -i

isort: ## sort imports
	./lint isort

black: ## format code
	./lint black

lint: clean autoflake isort black ## do autoflake, isort and black