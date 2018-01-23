#!/bin/bash

cd ../
export PYTHONPATH=$(pwd):~/common/
pip install -r requirements.txt
cd source
python server.py
