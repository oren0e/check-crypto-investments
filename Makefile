FOLDERS:= backend tests

test:
	pytest -s -vvv -m "not integration" tests

test_all:
	pytest -s -vvv tests
