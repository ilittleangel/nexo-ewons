#!/usr/bin/env bash

run() {
    python3.6 pipeline.py
}

seconds=1

echo "Activando virtual enviroment: source ~/enviroments/monitor/bin/activate"
source ~/enviroments/monitor/bin/activate
cd ~/nexo-ewons
while true; do
    echo ""
    echo "---------------------"
    echo "ARRANCANDO INGESTION"
    echo "---------------------"
    echo ""
    run
    echo ""
    echo "---------------------"
    echo "DURMIENDO ${seconds} SEGUNDOS"
    echo "---------------------"
    sleep ${seconds}
done
