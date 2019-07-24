The following are example uses of grafapy. See examples.py for step by step descriptions of the code

# Example 1

Code:
```python
def example1(token):
   d = DashBoard(title="Example 1", token=token)

   host = "nutmeg"
   item = "Incoming network traffic on eth0"
   panelTitle = "Incoming network traffic for " + host

   q = Query(host, item)
   p = GraphPanel(title=panelTitle, queryArray=[q])
   d.addPanels([p])
   d.push()
```

Grafana:
![alt text](https://raw.githubusercontent.com/hrand1005/grafapyAPI/master/pictures/Example1.png "Example1")
Note: the above panel is one half the length of a grafana dashboard (panelsPerRow dashboard parameter defaults to 2)

# Example 2

Code:
```python
def example2(token):
   d = DashBoard(title="Example 2", token=token, panelsPerRow=3)
   
   hosts = ["nutmeg", "mustard", "tomato", "basil", "cheese", "lime", "flour", "cream", "mace"]
   item1 = "Incoming network traffic on eth0"
   item2 = "Outgoing network traffic on eth0"
   panels = []

   for host in hosts:
      q1 = Query(host, item1, alias="Incoming traffic")
      q2 = Query(host, item2, alias="Outgoing traffic")
      panelTitle = host + " network traffic on eth0"
      p = GraphPanel(title=panelTitle, queryArray=[q1, q2], units="bps")
      panels.append(p)

   d.addPanels(panels)
   d.push()
```

Grafana:
![alt text](https://raw.githubusercontent.com/hrand1005/grafapyAPI/master/pictures/Example2.png "Example2")
