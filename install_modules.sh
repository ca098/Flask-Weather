#!/bin/bash
#Build and run


echo Setting up Virtual Environment...

echo Start servers...
virtualenv env
source env/bin/activate
pip install flask
pip install flask-restful
pip install requests
pip install configparser

sh ./run.sh

