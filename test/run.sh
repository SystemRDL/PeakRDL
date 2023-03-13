#!/bin/bash

set -e

this_dir="$( cd "$(dirname "$0")" ; pwd -P )"

# Initialize venv
venv_bin=$this_dir/.venv/bin
python3 -m venv $this_dir/.venv
source $venv_bin/activate

# Install test dependencies
python -m pip install -U pip setuptools wheel
python -m pip install -U pytest pytest-cov coverage pylint mypy

# Install dut
cd $this_dir/../
python -m pip install .
cd $this_dir

# Run unit tests while collecting coverage
pytest --cov=peakrdl

# Generate coverage report
coverage html -i -d $this_dir/htmlcov

# Run lint
pylint --rcfile $this_dir/pylint.rc ../src/peakrdl

# Run static type checking
mypy $this_dir/../src/peakrdl
