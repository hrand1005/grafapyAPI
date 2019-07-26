The following are example uses of grafapy. See [examples.py](https://github.com/hrand1005/grafapyAPI/blob/master/examples/examples.py) for step by step descriptions of the code. Full documentation of objects/methods can be found in our [wiki](https://github.com/hrand1005/grafapyAPI/wiki).

### grafAuth
Our examples.py script reads in a [token and url](https://github.com/hrand1005/grafapyAPI/blob/ada917aa9e656fc327c6b473d65172e9f44b6c37/examples/examples.py#L174) from a file in the user's home directory formatted as follows:
```python
<token>
<URL>
```
You can run our examples.py script by creating such a file in your own home directory, or modifying the script to include your token and url via other means. More on Grafana tokens [here](https://grafana.com/docs/tutorials/api_org_token_howto/).

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

# Example 3

Code:
```python
def example3(token):
   d = DashBoard(title="Example 3", token=token, panelsPerRow=5, panelHeight=8)

   hosts = ["abra", "charmander", "meowth", "jigglypuff", "ponyta", "psyduck", "pikachu", "zubat", "beedrill", "bulbasaur"]
   item = "Number of logged in users"
   panels = []
   colors = ["green", "yellow", "red"]
   threshold = "1, 4"

   for host in hosts:
      q = Query(host, item)
      panelTitle = host + " users"
      p = SingleStatPanel(title=panelTitle, queryArray=[q], colors=colors, thresholds=threshold, colorBackground=True)
      panels.append(p)

   d.addPanels(panels)
   d.push()
```

Grafana:
![alt text](https://raw.githubusercontent.com/hrand1005/grafapyAPI/master/pictures/singleStat.png "Example3")

# Example 4

Code:
```python
def example4(token, URL):                                                                                                                                                                                                          [11/1838]
    d = DashBoard(title="Example 4", token=token, panelsPerRow=8, panelHeight=6)                                                                                                                                                       

    hosts = ["almond", "celery", "cabbage", "butter", "hyssop", "dill", "egg", "thyme", "coriander", "coconut", "cornstarch", "marjoram", "mace", "onion", "mustard", "parsley", "pepper", "sage", "milk", "honey", "poppy", "sesame",
"spinach", "lime", "licorice", "olive", "rosemary", "saffron"]

    item1 = "System uptime"
    item2 = "ICMP ping"
    panels = []
    colors = ["grey", "red", "yellow", "green"]
    threshold = "1, 1800, 172800"
    units = "s"
    decimals = 1
    math = "uptime*ping"
    link = URL + "grafana/d/3AcvQxVWk/any-single-machine-status?orgId=1&refresh=1m&var-Group=Linux%20servers&var-Host="

    hosts.sort()

    for host in hosts:
        q1 = Query(host, item1, alias="uptime")
        q2 = Query(host, item2, alias="ping")
        panelTitle = host + " uptime"
        absLink = link + host
        p = MathStatPanel(title=panelTitle, queryArray=[q1, q2], colors=colors, thresholds=threshold, units=units, decimals=decimals, math=math, colorBackground=True, absLink=absLink)
        panels.append(p)

    d.addPanels(panels)
    d.push()
```

Grafana:
![alt text](https://raw.githubusercontent.com/hrand1005/grafapyAPI/master/pictures/mathStat.png "Example4")

Notice the icons in the top right corners of the panels. If you hover over them, you can use the absolute link. In our case, thyme links to the following custom dashboard:

![alt text](https://raw.githubusercontent.com/hrand1005/grafapyAPI/master/pictures/thyme.png "thyme")
