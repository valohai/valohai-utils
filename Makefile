PYTHON := $(shell which python)

.PHONY: default mypy

default:
	@echo "Available targets:"
	@echo "=================="
	@echo
	@echo "mypy       - Run static type checking with mypy"

# Static type checking with mypy
mypy:
	mypy --python-executable="$(PYTHON)" .
