MYPY := $(shell which mypy)
PYTHON := $(shell which python)

.PHONY: default mypy

default:
	@echo "Available targets:"
	@echo "=================="
	@echo
	@echo "mypy       - Run static type checking with mypy"

# Static type checking with mypy
mypy:
ifeq ($(MYPY),)
	@echo "mypy not found, skipping"
else
	$(MYPY) --strict --python-executable="$(PYTHON)" .
endif
