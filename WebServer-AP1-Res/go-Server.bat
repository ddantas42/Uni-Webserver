@echo off
echo off

set FLASK_APP=Server.py

set FLASK_BIN=.env\Scripts\flask

start %FLASK_BIN% run --port 80 --host="0.0.0.0"

start http://localhost