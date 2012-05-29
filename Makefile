test:
	PYTHONPATH=. unit2 discover -s tests/

dist:
	python setup.py sdist

