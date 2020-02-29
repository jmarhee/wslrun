from setuptools import setup
setup(name='wslrun',
version='0.1',
description='Testing Framework powered by Windows Subsystem for Linux (WSL)',
url='https://gitlab.com/jmarhee/wslrun',
author='jmarhee',
author_email='jmarhee@interiorae.com',
license='MIT',
packages=['wslrun'],
scripts=['bin/wslrun'],
install_requires=[
    'pprint',
],
zip_safe=False)