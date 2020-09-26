dist:
	python setup.py build --plat-name=win-amd64 bdist 
# 	python setup.py build --plat-name=win-amd64 bdist_wininst

.SILENT:
tag-release:
	if [[ $(TAG) == v?.?.? ]]; then echo "Tagging $(TAG)"; elif [[ $(TAG) == v?.?.?? ]]; then echo "Tagging $(TAG)"; else echo "Bad Tag Format: $(TAG)"; exit 1; fi && git tag -a $(TAG) -m "Releasing $(TAG)" ; read -p "Push tag: $(TAG)? " push_tag ; if [ "${push_tag}"="yes" ]; then git push origin $(TAG); fi

push-test:
	python -m twine upload --config-file ~/.pypirc.ini --repository testpypi dist/*

push:
	python -m twine upload --config-file ~/.pypirc.ini dist/*

install:
	pip3 install -e .
