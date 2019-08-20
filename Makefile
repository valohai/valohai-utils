prettify:
	black .
	isort -rc .

lint:
	flake8 .
	black --check .
	isort -rc -c .