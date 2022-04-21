#!/bin/sh
virtualenv -p /usr/bin/python3 env
./env/bin/activate
pip install -r requirements.txt