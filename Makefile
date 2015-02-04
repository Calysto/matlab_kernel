# Note: This is meant for Metaernel developer use only
.PHONY: all clean test test_warn cover release gh-pages

export TEST_ARGS=--exe -v --with-doctest
export NAME=matlab_kernel
export VERSION=`python -c "import $(NAME); print($(NAME).__version__)"`
export GHP_MSG="Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`"

all: install

install: clean
	python setup.py install

install3: clean
	python3 setup.py install

clean:
	rm -rf build
	rm -rf dist
	/usr/bin/find . -name "*.pyc" -o -name "*.py,cover"| xargs rm -f

demo: clean
	python setup.py install
	ipython qtconsole --kernel $(NAME)

test: clean
	python setup.py install
	cd; nosetests $(TEST_ARGS)
	make clean

test_warn: clean
	python setup.py install
	export PYTHONWARNINGS="all"; cd; nosetests $(TEST_ARGS)
	make clean

cover: clean
	pip install nose-cov
	nosetests $(TEST_ARGS) --with-cov --cov $(NAME) $(NAME)
	coverage annotate

release: test
	pip install wheel
	python setup.py register
	python setup.py sdist --formats=gztar,zip upload
	git tag v$(VERSION)
	git push origin --all

gh-pages: clean
	pip install sphinx-bootstrap-theme numpydoc sphinx ghp-import
	git checkout master
	git pull origin master
	make -C docs html
	ghp-import -n -p -m $(GHP_MSG) docs/_build/html