.PHONY: all test


test:
	python setup.py install --user
	ipython console --kernel=matlab_kernel

all:
	python setup.py register
	python setup.py sdist --formats=gztar,zip upload
