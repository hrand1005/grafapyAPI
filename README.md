# grafapyAPI
Python API for creating Grafana Dashboards using Zabbix as a datasource.

# Version 0.1, Getting Started
Everything you need to use grafapy can be found in the API directory. Simply change the postURL in dashboard.py's push() method to match your own grafana URL, and you're ready to start creating your own dashboards.

# What is it?
Grafapy is a python-grafana API that specializes in creating dashboards with myriad panels of a single size. The API allows a user to configure grafana pages using dashboard, panel, and query objects instead of working with a JSON.

For example, this...
```python
host="nutmeg"                                        #host and item names defined according to
item="Processor Load (1 min average per core)"       #their configuration in zabbix
q = Query(host, item)
p = GraphPanel(title='MyPanel', queryArray=[q])
d = DashBoard(title='MyDash', token=token)
d.addPanels([p])
d.push()
```
produces this...

![alt text](https://raw.githubusercontent.com/hrand1005/grafapyAPI/master/pictures/MyDash.png "MyDash")

# Supported Panel Types
-Graph Panel

-Single Stat Panel

-Math Panel (Singlestat)

# When should I use it?
Grafana already provides templating that allows users to view various stats for selected hosts and host groups. But what if you want to check which of your machines are up? A glance at each machine's CPU Load? A quick look at each machine's network traffic? These types of checks are invaluable for catching irregularities in your network, and this is where grafapy shines. 

![alt text](https://raw.githubusercontent.com/hrand1005/grafapyAPI/master/pictures/gpuOverview.png "GPU Overview")
![alt text](https://raw.githubusercontent.com/hrand1005/grafapyAPI/master/pictures/cpuLoads.png "CPU Loads")
![alt text](https://raw.githubusercontent.com/hrand1005/grafapyAPI/master/pictures/systemUptimes.png "System uptimes")

See 'examples' for example uses of grafapy.
