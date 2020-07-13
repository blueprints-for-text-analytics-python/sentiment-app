#!/bin/bash
source activate sentiment-app 
gunicorn -w 3 -b :5000 -t 30 "app:run_app()"
