#!/bin/bash

set -e
cd "$(dirname "$0")"

# Initialize venv
python3.11 -m venv .venv
source .venv/bin/activate

# Install test dependencies
python -m pip install -r requirements.txt

# Install CLI first, then bundle toolchain pkg
python -m pip install ../peakrdl-cli/
python -m pip install ../peakrdl/

# Run unit tests while collecting coverage
pytest --cov=peakrdl

# Generate coverage report
coverage html -i -d htmlcov

# Run lint
pylint --rcfile pylint.rc ../peakrdl-cli/src/peakrdl

# Run static type checking
mypy ../peakrdl-cli/src/peakrdl
