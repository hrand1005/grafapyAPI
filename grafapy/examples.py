#!/usr/bin/python3
"""
Examples for grafaPy API.
"""
from dashboard import *
from panel import *
import os
import sys

def getCredentials(grafAuth):
    try:
        inFile = open(grafAuth, "r")
        token = inFile.readline().strip()
        URL = inFile.readline().strip()
        inFile.close()
    except IOError:
        print("Couldn't open %s..." % grafAuth)
        sys.exit(0)
    return token, URL

def example1(token):
    """
    This simple example covers how to create Query, Panel, and DashBoard Objects. 
    """
    #create a new dashboard object
    d = DashBoard(title="Example 1", token=token)

    #define hosts and items according to their configuration in zabbix
    host="nutmeg"
    item="Incoming network traffic on eth0"

    #you may want to use these variables in your panel title!
    panelTitle = "Incoming network traffic for " + host

    #create a new query object
    q = Query(host, item)

    #for a graph of your data, create a GraphPanel object, including your query in the constructor
    p = GraphPanel(title=panelTitle, queryArray=[q])

    #simply add your created panel to your dashboard, and push it to grafana!
    #note that we provide a postURL for our push method because we didn't set a url in the dashboard constructor
    #see example 2 for an alternative way of providing a postURL
    d.addPanels([p])
    d.push(postURL="http://localhost:3000/api/dashboards/db")

def example2(token):
    """
    This example improves on example 1 by exploring more features of the GraphPanel and DashBoard objects
    """
    #create a new dashboard object, and set panelsPerRow equal to 3
    #let's set the url in the constructor for this example
    d = DashBoard(title="Example 2", url="http://localhost:3000/api/dashboards/db", token=token, panelsPerRow=3)

    #let's make a dashboard with multiple hosts
    hosts = ["nutmeg", "mustard", "tomato", "basil", "cheese", "lime", "flour", "cream", "mace"]

    #let's create graphs that show both incoming and outgoing network traffic
    item1 = "Incoming network traffic on eth0"
    item2 = "Outgoing network traffic on eth0"

    #declare a list to store your created panels
    panels = []

    for host in hosts:
        #use the alias parameter to change the keys that show up on your graph panels
        q1 = Query(host, item1, alias="Incoming traffic")
        q2 = Query(host, item2, alias="Outgoing traffic")

        panelTitle = host + " network traffic on eth0"

        #pass in units as grafana requires, in this case 'bps' is bytes per second
        p = GraphPanel(title=panelTitle, queryArray=[q1, q2], units="bps")
        panels.append(p)

    #add the panels to your dasbhoard, and push
    #notice that push doesn't requrie a postURL, since one was provided in the dashboard's constructor
    d.addPanels(panels)
    d.push()

def example3(token):
    """
    This example introduces singlestat panels, which can be heavily customized.
    """
    #create a new dashboard object, and set panelsPerRow equal to 5, and panelHeight equal to 8
    d = DashBoard(title="Example 3", token=token, url="http://localhost:3000/api/dashboards/db",panelsPerRow=5, panelHeight=8)

    #let's make this dashboard with multiple hosts
    hosts = ["abra", "charmander", "meowth", "jigglypuff", "ponyta", "psyduck", "pikachu", "zubat", "beedrill", "bulbasaur"]

    #singlestat can only display one query
    item = "Number of logged in users"

    #declare a list to store your panels
    panels = []

    #declare a list of colors that will represent different states of your hosts
    colors = ["green", "yellow", "red"]

    #declare a threshold string that you want to correspond to your colors. in this case, 0 logged on users is green,
    #1-3 is yellow, and 4 or above is red
    threshold = "1, 4"

    for host in hosts:
        q = Query(host, item)
        
        panelTitle = host + " users"
        #set colors and thresholds equal to our declared variables, and colorBackground to True
        p = SingleStatPanel(title=panelTitle, queryArray=[q], colors=colors, thresholds=threshold, colorBackground=True)
        panels.append(p)

    #add panels to your dashboard, and push
    d.addPanels(panels)
    d.push()

def example4(token, URL):
    """
    This example introduces mathpanels, a subclass of singlestat panels, and absolute links.
    While it might seem appropriate to just use a singleStat panel in this case, our zabbix item
    for uptime returns no values if the machine is down, because the zabbix agent can't be reached.
    We'll use a second item, ICMP ping, in conjunction with system uptime to work around this using
    the math panel. ICMP ping returns 0 when a system can't be pinged, and 1 when it can be pinged.
    This allows us to multiply system uptime by ICMP ping to get an appropriate value to display
    in grafana.
    """
    #create a new dashboard object, and set panelsPerRow equal to 5, and panelHeight equal to 8
    d = DashBoard(title="Example 4", token=token, url="http://localhost:3000/api/dashboards/db", panelsPerRow=8, panelHeight=6)
    
    #we'll iterate through a list of hosts again
    hosts = ["almond", "celery", "cabbage", "butter", "hyssop", "dill", "egg", "thyme", "coriander", "coconut", "cornstarch", "marjoram", "mace", "onion", "mustard", "parsley", "pepper", "sage", "milk", "honey", "poppy", "sesame", "spinach", "lime", "licorice", "olive", "rosemary", "saffron"]

    #declare item variables to be used in each of our queries
    item1 = "System uptime"
    item2 = "ICMP ping"

    #declare a list to store your panels
    panels = []

    #declare a list of colors that will represent different ranges of uptimes for your hosts
    colors = ["grey", "red", "yellow", "green"]

    #define a threshold as you would in a singlestat panel (we'll be using seconds as our unit, so these correspond to 1 second, half an hour, and two days)"
    threshold = "1, 1800, 172800"

    #define your units
    units = "s"

    #how many decimals?
    decimals = 1

    #make a string for your mathematical computation. the math panel uses your queries' aliases as
    #variable names, so we'll have to set the aliases to 'uptime' and 'ping' in the query constructor
    math = "uptime*ping"

    #value map?
    valueMap=  [{
                  "op": "=",
                  "text": "Down :(",
                  "value": "null"
                },
                {
                  "op": "=",
                  "text": "Down :(",
                  "value": "0"
                },
                {
                  "op": "=",
                  "text": "Up :)",
                  "value": "1"
                }]

    #perhaps we'll want to see details about our hosts individually by clicking on them. this can be accomplished by creating an absolute link to another dashboard
    #we'll link our hosts to one of our templated dashboards that shows various stats about a single machine, and when we iterate through our hosts, we'll tweak the 
    #link so that each host links to their own individual dashboard
    link = URL + "grafana/d/3AcvQxVWk/any-single-machine-status?orgId=1&refresh=1m&var-Group=Linux%20servers&var-Host="

    #let's sort our hosts so that our dashboard shows them in alphabetical order
    hosts.sort()
    #iterate through yours hosts, and create your panels
    for host in hosts:
        #don't forget to set your aliases!
        q1 = Query(host, item1, alias="uptime")
        q2 = Query(host, item2, alias="ping")

        panelTitle = host + " uptime"
        absLink = link + host
        p = MathStatPanel(title=panelTitle, queryArray=[q1, q2], colors=colors, thresholds=threshold, valueMaps=valueMap, units=units, decimals=decimals, math=math, colorBackground=True, absLink=absLink)
        panels.append(p)

    #add panels to your dashboard, and push
    d.addPanels(panels)
    d.push()

def main():
    grafAuth = os.environ["HOME"] + "/grafanaToken"
    token, URL = getCredentials(grafAuth)
    example1(token)
    example2(token)
    example3(token)
    example4(token, URL)
main()

