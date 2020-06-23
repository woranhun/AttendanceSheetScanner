#!/bin/bash
sudo apt update -y
sudo apt install tesseract-ocr -y
sudo apt install libtesseract-dev -y
sudo apt install tesseract-ocr-hun -y

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
