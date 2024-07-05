@echo off
pip install -r requirements.txt  >nul 2>&1
python app/app.py
pause