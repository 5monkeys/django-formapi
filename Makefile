test:
	python setup.py test

flake8:
	flake8 --ignore=E501,E225,E128,W391,W404,W402 --exclude migrations --max-complexity 12 formapi

install:
	python setup.py install

develop:
	python setup.py develop

coverage:
	coverage run --include=formapi/* setup.py test
