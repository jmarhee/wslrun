from setuptools import setup
setup(name='py-wslrun',
version='0.1.2',
description='Testing Framework powered by Windows Subsystem for Linux (WSL)',
url='https://git-central.openfunction.co/jmarhee/wslrun',
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
install_requires=[
	"pyyaml"
],
zip_safe=False)
