# grafapyAPI
Python API for creating Grafana Dashboards using Zabbix as a datasource.

# What is it?
Grafapy is a python-grafana API that specializes in creating dashboards with myriad panels of a single size. The API allows a user to configure grafana pages using dashboard, panel, and query objects instead of working with a JSON.

For example, this...
```python
host="nutmeg"
item="Processor Load (1 min average)"       #host and item names defined according to how they're configured in zabbix
q = Query(host, item)
p = GraphPanel(title='MyPanel', queryArray=[q])
d = DashBoard(title='MyDash', token=token)
d.addPanels([p])
d.push()
```
produces this...
