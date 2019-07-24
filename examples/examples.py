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
    d.addPanels([p])
    d.push()

def example2(token):
    """
    This example improves on example 1 by exploring more features of the GraphPanel and DashBoard objects
    """
    #create a new dashboard object, and set panelsPerRow equal to 3
    d = DashBoard(title="Example 2", token=token, panelsPerRow=3)

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
    d.addPanels(panels)
    d.push()

def main():
    grafAuth = os.environ["HOME"] + "/grafanaToken"
    token, URL = getCredentials(grafAuth)
    example1(token)
    example2(token)
main()

