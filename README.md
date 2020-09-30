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

* load &lt;file&gt;: Load file into memory.
* print [&lt;var&gt;]: Print a list with IPs in memory. e.g.: print A1
* geoip [&lt;ip&gt; | &lt;range&gt; | all]: Geo-location lookup tool. e.g.: range(0:10)
* rdap [&lt;ip&gt; | &lt;range&gt; | all]: Registration data access search for IP. e.g.: range(0:10)
* find &lt;regex:ip&gt;: A regex query to search IP addresses. e.g.: find .*50
* help: Prints help dialog.
* exit: Exit.
