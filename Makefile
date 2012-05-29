test:
	PYTHONPATH=. unit2 discover -s tests/

dist:
	python setup.py sdist

publish:
	python setup.py sdist bdist_egg upload

