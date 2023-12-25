#!/bin/sh
export FLASK_APP=./url-shortener-flask/main.py
flask --debug run -h 0.0.0.0