#!/bin/sh

virtualenv hardwareTests
source hardwareTests/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt

python test/hardwareTests.py

rm -rf hardwareTests

