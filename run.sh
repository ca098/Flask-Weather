#!/bin/bash
#Build and run


echo Setting up Virtual Environment...

echo Start servers...
gnome-terminal -e 'sh -c "source env/bin/activate;python ClientWebsite/app.py;exec bash"'
gnome-terminal -e 'sh -c "source env/bin/activate;python DistAPI/src/server.py;exec bash"'
sleep 3s
gnome-terminal -e 'sh -c "echo Launching browser window;firefox --new-window http://127.0.0.1:8500/"'

