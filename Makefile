folders = backend tests

test:
	pytest -s -vvv -m "not integration" tests

test_all:
	pytest -s -vvv tests

check_format:
	black --check $(folders)
	isort **/*.py --check-only

do_format:
	black $(folders)
	isort **/*.py

lint:
	pylint $(folders)
	mypy $(folders)
