
## Making a release

Tag the release using `git tag`, then:

```
rm -rf dist
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/*
```
