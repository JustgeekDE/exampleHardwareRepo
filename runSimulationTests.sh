#!/bin/sh

virtualenv simulationTests
source simulationTests/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt

python test/simulationTests.py

rm -rf simulationTests

