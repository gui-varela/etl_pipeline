#!/bin/bash
cd /caminho/para/seu/projeto
source venv/bin/activate  # Ative o virtualenv se estiver usando
python main.py >> logs/etl_$(date +\%F).log 2>&1
