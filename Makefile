# Note: This is meant for octave_kernel developer use only
.PHONY: all clean test release

export NAME=`python setup.py --name 2>/dev/null`
export VERSION=`python setup.py --version 2>/dev/null`

all: clean
	python setup.py install

clean:
	rm -rf build
	rm -rf dist

test: clean
	python setup.py build
	python -m matlab_kernel install

release: test clean
	pip install wheel
	git commit -a -m "Release $(VERSION)"; true
	git tag v$(VERSION)
	rm -rf dist
	python setup.py register
	python setup.py bdist_wheel --universal
	python setup.py sdist
	git push origin --all
	git push origin --tags
	twine upload dist/*
