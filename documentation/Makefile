.PHONY: deps
deps:
	uv venv
	uv pip compile requirements.in -o requirements.txt
	uv pip install -r requirements.txt

.PHONY: serve
serve:
	mkdocs serve

.PHONY: build
build:
	mkdocs build
