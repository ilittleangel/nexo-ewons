#!/usr/bin/env bash

run() {
    python3.6 ~/nexo-ewons/pipeline.py
}

source ~/venv/bin/activate
while true; do run; done
