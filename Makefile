dist:
	python setup.py build --plat-name=win-amd64 bdist 
# 	python setup.py build --plat-name=win-amd64 bdist_wininst

tag-release:
	git tag -a $(TAG) -m "Releasing $(TAG)" ; git push origin $(TAG)

push-test:
	python -m twine upload --config-file ~/.pypirc.ini --repository testpypi dist/*

push:
	python -m twine upload dist/*

install:
	pip3 install -e .
