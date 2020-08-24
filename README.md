# Flask Weather API

The DistAPI directory contains a REST API that handles a POST from the client and parses the data into
an imperial format. The ClientWebsite directory holds a website that sends data to this service and handles the response.

## Installation

1.) In a terminal window execute 
```bash
./install_modules.sh
``` 
and it will automatically install the required modules and run each server whilst also opening up a browser window 
for the client application. You may need to make the script executable with 
```bash
chmod +x install_modules.sh 
```
This script will also only work on Linux operating systems, gnome-terminal in run.sh is used as a terminal window
to run both servers and it is not accessible on MacOS.

This script is configured to open up firefox on the DEC-10 machines so if it isn't installed on your machine 
you will have to open a browser manually and locate to http://127.0.0.1:8500/

2.) If installation 1 fails. Then in a terminal window at the top level directory enter these commands:

```bash
virtualenv env
source env/bin/activate

pip install flask
pip install flask-restful
pip install requests
pip install configparser
```

## Usage

Providing that installation 1 did not work, open up two more terminal windows for the API and client web server and enter in:

```bash
source env/bin/activate
```
To each one, then navigate to each of the directories and run the python files.

ClientWebsite -> app.py

DistAPI -> src  -> server.py

```bash
python server.py

python app.py
```

The API should be running on http://127.0.0.1:5000/

The website should be running on http://127.0.0.1:8500/
