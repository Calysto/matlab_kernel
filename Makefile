# Note: This is meant for octave_kernel developer use only
.PHONY: all clean test release

export NAME=`python setup.py --name 2>/dev/null`
export VERSION=`python setup.py --version 2>/dev/null`

all: clean
	pip install .

clean:
	rm -rf build
	rm -rf dist

test: clean
	pip install .
	python -c "from jupyter_client.kernelspec import find_kernel_specs; assert 'matlab' in find_kernel_specs()"

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
