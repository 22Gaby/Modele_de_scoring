#!/bin/sh
rm -rf dev-env
virtualenv --python=/usr/bin/python3.8 dev-env
. ./dev-env/bin/activate
pip install -r requirements.txt
