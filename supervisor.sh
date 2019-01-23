#!/usr/bin/env bash

if [ ! -f "venv/bin" ]; then
        virtualenv "venv"
        . venv/bin/activate
else
        . venv/bin/activate
fi
#exec gunicorn -w 4 -b 127.0.0.1:8081 scoremodel:app --timeout 240 --graceful-timeout 240 --capture-output --error-logfile gunicorn_error.log
exec gunicorn -w 4 -b 127.0.0.1:8081 scoremodel:app --timeout 240 --graceful-timeout 240 

