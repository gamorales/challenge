# Python Challenge
Given a set of IPs, perform Geo IP and RDAP lookups, and accept a query to filter results. 

## Installing
User must create a virtual environment with:
```
python3 -m venv venv
```

Then, activate the virtual environment and install the dependencies within file requirement.txt:
```
source venv/bin/activate
```
```
pip3 install -r requirements.txt
```

## Usage
Once everything had been installed correctly, must executed the main.py file:
```
python3 main.py
``` 

## Commands
The application runs like a command-line interface, these are the commands that allows work with the loaded IPs 

* load <file>: Load file into memory.
* print: Print a list with IPs in memory.
* geoip [<ip> | <range> | all]: Geo-location lookup tool. Ej: range(0:10)
* rdap [<ip> | <range> | all]: Registration data access search for IP. Ej: range(0:10)
* find <regex:ip>: A regex query to search IP addresses. Ej: find .*50
* help: Prints help dialog.
* exit: Exit.
