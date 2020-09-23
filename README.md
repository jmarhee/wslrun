WSLrun
===
[![Build status](https://ci-central.openfunction.co/api/projects/status/6e2tsa5mh5k4s3el?svg=true)](https://ci-central.openfunction.co/project/AppVeyor/wslrun) [![PyPI version](https://badge.fury.io/py/py-wslrun.svg)](https://badge.fury.io/py/py-wslrun)

A Windows Subsystem for Linux (WSL)-based testing framework written in Python. 

## Prerequisites

WSL must be installed on your machine, and presently, WSL distros you wish to use in your pipeline definitions will need to currently be installed (i.e. `Ubuntu`, `Alpine`, and installed under that name).

## Installation

Clone this repo, and install from source:

```powershell
pip install -e .
```
or from PyPi:

```powershell
pip install py-wslrun
```

and run the CLI:

```
wslrun --pipeline your_config.json
```

## Usage

Define a pipeline in your project directory:

```json
{
    "name": "PS Test",
    "description": "Tests building in multiple environments",
    "pullPolicy": "Never",
    "ciMode": "False",
    "stages": [
        {
            "image": "AlpineDub",
            "name": "Build on distro with a passing job",
            "steps": [
                "sudo apk --update add musl-dev",
                "env CGO_ENABLED=1 GOOS=linux GOARCH=amd64 go build -v -x -o package-amd64-alpine"
            ]
        },
        {
            "image": "UbuntuDub",
            "name": "Build on distro I know will fail",
            "steps": [
                "GOOS=linux GOARCH=amd64 go build -v -x -o package-amd64-ubuntu"
            ]
        },
        {
            "image": "AlpineLub",
            "name": "Build on image I know doesn't exist",
            "steps": [
                "env GOOS=linux GOARCH=amd64 go build -v -x -o package-amd64-alpine"
            ]
        }
    ]
}
```
or in YAML:

```yaml
---
name: PS Test
description: Tests building in multiple environments
pullPolicy: Never
ciMode: 'False'
stages:
- image: AlpineDub
  name: Build on distro with a passing job
  steps:
  - sudo apk --update add musl-dev
  - env CGO_ENABLED=1 GOOS=linux GOARCH=amd64 go build -v -x -o package-amd64-alpine
- image: UbuntuDub
  name: Build on distro I know will fail
  steps:
  - GOOS=linux GOARCH=amd64 go build -v -x -o package-amd64-ubuntu
- image: AlpineLub
  name: Build on image I know doesn't exist
  steps:
  - GOOS=linux GOARCH=amd64 go build -v -x -o package-amd64-alpine
```

For each stage, an `image`, `name`, and list of `steps` will be required.

Run the test (for example, as a pre-commit hook) with:

```
wslrun --pipeline build.json
```

and see the test results report, which will look like this:

```powershell
PS C:\Users\you\repos\project> python .\wslrun --pipeline .\build.json
wslExec (image: AlpineDub): sudo apk --update add musl-dev
✔️: sudo apk --update add musl-dev

wslExec (image: AlpineDub): go build
✔️: go build

🔔: Build on distro with a passing job completed.
Pipeline completed:

🧾 Report: Build on distro with a passing job...

{'completions': '2/2'}


🧾 Report: Build on distro I know will fail...

{'completions': '0/0, Image Unavailable: 1'}


🧾 Report: Build on image I know doesn't exist...

{'completions': '0/0, Image Unavailable: 4294967295'}


Completed.
```

## Forthcoming Enhancements

1. Remote testing mode for Server 2019 in progress (part of a CI/CD offering).
2. Image/Distro registry and management in progress. 
