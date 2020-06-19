#!/bin/bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
