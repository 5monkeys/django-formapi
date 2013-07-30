test:
	python setup.py test

flake8:
	flake8 --ignore=E501,E128 --exclude migrations --max-complexity 12 formapi

install:
	python setup.py install

develop:
	python setup.py develop

coverage:
	coverage run --include=formapi/* setup.py test
