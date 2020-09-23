WSLrun
===
[![Build status](https://ci-central.openfunction.co/api/projects/status/6e2tsa5mh5k4s3el?svg=true)](https://ci-central.openfunction.co/project/AppVeyor/wslrun) [![PyPI version](https://badge.fury.io/py/wslrun.svg)](https://badge.fury.io/py/wslrun)

A Windows Subsystem for Linux (WSL)-based testing framework written in Python. 

## Prerequisites

WSL must be installed on your machine, and presently, WSL distros you wish to use in your pipeline definitions will need to currently be installed (i.e. `Ubuntu`, `Alpine`, and installed under that name).

## Installation

Clone this repo, and install from source:

```powershell
pip install -e .
```

and run the CLI:

```
wslrun
```

## Usage

Define a pipeline in your project directory:

```json
{
    "name": "PS Test",
    "description": "Tests building in multiple environments",
    "stages": [
        {
            "image": "Alpine",
            "name": "Install",
            "steps": [
                "sudo apk --update add musl-dev",
                "sudo apk install -y package"
            ]
        },
        {
            "image": "Ubuntu",
            "name": "Install-Ubuntu",
            "steps": [
                "apt install -y package"
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
stages:
- image: Alpine
  name: Install
  steps:
  - sudo apk --update add musl-dev
  - sudo apk install -y package
- image: Ubuntu
  name: Install-Ubuntu
  steps:
  - apt install -y package
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
