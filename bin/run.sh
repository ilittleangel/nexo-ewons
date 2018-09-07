#!/usr/bin/env bash

run() {
    python3.6 pipeline.py
}

echo "Activando virtual enviroment: source ~/enviroments/monitor/bin/activate"
source ~/enviroments/monitor/bin/activate
cd ~/nexo-ewons
while true; do
    echo "ARRANCANDO INGESTION";
    run;
    echo "DURMIENDO 30 SEGUNDOS";
    sleep 30;
done

