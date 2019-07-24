# grafapyAPI
Python API for creating Grafana Dashboards using Zabbix as a datasource.

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

See 'examples' for example uses of grafapy.
