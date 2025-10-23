.PHONY: cp-readme
cp-readme:
	cp ../README.md docs/index.md

.PHONY: deps
deps:
	uv venv
	uv pip compile requirements.in -o requirements.txt
	uv pip install -r requirements.txt

.PHONY: serve
serve: cp-readme
	mkdocs serve

.PHONY: build
build: cp-readme
	mkdocs build
