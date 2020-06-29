#!/bin/bash
sudo apt update -y
sudo apt install tesseract-ocr -y
sudo apt install libtesseract-dev -y
sudo apt install tesseract-ocr-hun -y
sudo apt install python3-tk -y

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
