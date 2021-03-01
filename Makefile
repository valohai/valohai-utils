prettify:
	black .
	isort .

lint:
	flake8 .
	black --check .
	isort -c .