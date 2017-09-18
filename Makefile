install:
	python3 setup.py install --user

test:
	py.test

cover:
	py.test --cov=wcf
