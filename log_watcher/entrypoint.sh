#!/bin/sh
set -x

service nginx start

echo "Nginx UP"

cd /home/app/ && python -u main.py