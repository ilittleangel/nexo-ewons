#!/usr/bin/env bash

run() {
    python3.6 pipeline.py
}

echo "Activando virtual enviroment: source ~/venvs/python3.6/bin/activate"
source ~/venvs/python3.6/bin/activate
cd ~/nexo-ewons
run
