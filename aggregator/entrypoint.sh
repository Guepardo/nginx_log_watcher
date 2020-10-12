#!/bin/sh
set -x

export FLASK_APP=main.py
cd /home/app/ && flask run --host=0.0.0.0