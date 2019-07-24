The following are example uses of grafapy. See examples.py for step by step descriptions of the code

# Example 1

Code:
```python
def example1(token):
   d = DashBoard(title="Example 1", token=token)

   host="nutmeg"
   item="Incoming network traffic on eth0"
   panelTitle="Incoming network traffic for "+host

   q = Query(host, item)
   p = GraphPanel(title=panelTitle, queryArray=[q])
   d.addPanels([p])
   d.push()
```

Grafana:
![alt text](https://raw.githubusercontent.com/hrand1005/grafapyAPI/master/pictures/Example1.png "Example1")
