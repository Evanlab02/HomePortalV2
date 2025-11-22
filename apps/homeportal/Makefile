.PHONY: requirements
requirements:
	uv pip compile requirements.in -o requirements.txt
	uv pip compile requirements.dev.in -o requirements.dev.txt

.PHONY: requirements-upgrade
requirements-upgrade:
	uv pip compile requirements.in --upgrade -o requirements.txt
	uv pip compile requirements.dev.in --upgrade -o requirements.dev.txt


.PHONY: deps
deps:
	uv pip install -r requirements.dev.txt

.PHONY: clean
clean:
	@rm -rf .mypy_cache \
	**/__pycache__ \
	**/**/__pycache__ \
	.coverage \
	.pytest_cache \
	build/ \
	dist/ \
	*.egg-info \
	coverage.xml \
	htmlcov \

.PHONY: format
format:
	@black .
	@isort . --profile black

.PHONY: lint
lint:
	@black --check .
	@isort . --check-only --profile black
	@flake8 . --max-line-length=100
	@mypy .

.PHONY: test
test:
	@pytest . --cov=. --no-cov-on-fail --cov-report term-missing
	@coverage xml
	@coverage html

.PHONY: fresh
fresh:
	rm -rf db.sqlite3
	python manage.py makemigrations
	python manage.py migrate
	python manage.py populate_history --auto

.PHONY: superuser
superuser:
	python manage.py createsuperuser

.PHONY: migrations
migrations:
	python manage.py makemigrations
