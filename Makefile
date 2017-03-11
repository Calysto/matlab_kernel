# Note: This is meant for octave_kernel developer use only
.PHONY: all clean test release

export NAME=matlab_kernel
export VERSION=`python -c "import $(NAME); print($(NAME).__version__)"`

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
	python setup.py register
	python setup.py bdist_wheel --universal
	python setup.py sdist
	git tag v$(VERSION)
	git push origin --all
	git push origin --tags
	twine upload dist/*
