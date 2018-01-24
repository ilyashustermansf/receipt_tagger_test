#!/bin/bash

python3.6 -m pip install -r requirements.txt
export PYTHONPATH=/home/ubuntu:/home/ubuntu/common
cd source
python3.6 server.py
