from setuptools import setup
setup(name='py-wslrun',
version='0.1.5',
description='Testing Framework powered by Windows Subsystem for Linux (WSL)',
url='https://github.com/jmarhee/wslrun',
author='jmarhee',
author_email='jmarhee@interiorae.com',
license='MIT',
packages=['wslrun'],
scripts=['bin/wslrun_test'],
entry_points = {
    "console_scripts": [
        "wslrun = wslrun:main",
    ]
},
python_requires='>=3',
install_requires=[
	"pyyaml"
],
zip_safe=False)
