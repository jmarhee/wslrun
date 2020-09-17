dist:
	rm -rf dist/ ; python setup.py bdist_wheel

tag-release:
	git tag -a $(TAG) -m "Releasing $(TAG)" ; git push origin $(TAG)

push-test:
	python3 -m twine upload --repository testpypi dist/*	

push:
	python3 -m twine upload dist/*

install:
	pip3 install -e .

