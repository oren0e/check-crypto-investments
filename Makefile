FOLDERS:= backend tests

test:
	pytest -s -vvv -m "not integration" tests

test_all:
	pytest -s -vvv tests

check_format:
	black --check FOLDERS
	isort **/*.py --check-only

do_format:
	black FOLDERS
	isort **/*.py

lint:
	pylint FOLDERS
	mypy FOLDERS
