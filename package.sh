#
rm -r build baai_modelhub.egg-info dist
python setup.py build
python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*