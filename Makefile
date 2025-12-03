MYPY := $(shell which mypy)

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
	$(MYPY) --strict .
endif
