#!/bin/bash

cd ../
python3.6 -m pip install -r requirements.txt
export PYTHONPATH=$(pwd):~/common/
cd source
python3.6 server.py
