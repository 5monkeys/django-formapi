test:
	python setup.py test

lint:
	flake8

install:
	python setup.py install

develop:
	python setup.py develop

coverage:
	coverage run --include=formapi/* setup.py test
	coverage report
