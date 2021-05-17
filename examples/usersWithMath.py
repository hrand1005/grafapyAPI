#!/usr/bin/python3
"""
Herbie Rand
"""
from dashboard import *
from panel import *
from pyzabbix import ZabbixAPI
import json   
import requests
import os     
import sys   
            
def getCredentials(zabAuth, grafAuth):
    """                              
    Parameters: Zabbix Authentication file with two lines,
        <URL>                                            
        <username>                                      
        <password>                                     
    Grafana Authentication file with two lines,       
        <token>                                      
        <URL>                                       
    Returns: ZabbixAPI Object, token, and url      
    """                                           
    zabbixAPI = None                             
    try:                                        
        inFile = open(zabAuth, "r")            
        ZURL = inFile.readline().strip()      
        username = inFile.readline().strip() 
        password = inFile.readline().strip()
        print(ZURL)                         
        print(username)                    
        inFile.close()                    
    except IOError:
        print("Couldn't open %s..." % zabAuth)
        sys.exit(0)

    zabbixAPI = ZabbixAPI(ZURL)
    zabbixAPI.login(username, password)
    print("Zabbix API version = " + zabbixAPI.api_version())

    try:
        inFile = open(grafAuth, "r")
        token = inFile.readline().strip()
        URL = inFile.readline().strip()
        inFile.close()
    except IOError:
        print("Couldn't open %s..." % grafAuth)
        sys.exit(0)

    return zabbixAPI, token, URL

def getHosts(zabbixAPI, group):
    """
    Parameters: zabbixAPI object
    Returns: a list of zabbix hosts from the provided group
    """
    zabbixGroup = zabbixAPI.hostgroup.get(output=["groupid"], filter={"name":[group]})
    groupID = [zabbixGroup[0]["groupid"]]
    myGroup = zabbixAPI.host.get(output=["host"], groupids=groupID)
    hostNames = []
    for host in myGroup:
        hostNames.append(host["host"])
    hostNames.sort()
    return hostNames

def main():
    zabAuth = os.environ["HOME"] + "/zabbixAuth"
    grafAuth = os.environ["HOME"] + "/grafanaToken"
    zabbixAPI, token, url = getCredentials(zabAuth, grafAuth)
    hosts = getHosts(zabbixAPI, "Lab_240")
    url += "/api/dashboards/db"
    d = DashBoard(title="Users Per Lab", token=token, url=url)
    groups = ["Lab_238", "Lab_240", "Lab_252", "Lab_256","Lab_Clothier"]
    for group in groups:
        hosts = getHosts(zabbixAPI, group)
        queries = []
        queries2 = []
        math = ""
        math2 = ""
        for host in hosts:
            q = Query(host, "Number of logged in users", alias=host)
            queries.append(q)
            math+= host + "+"
            q2 = Query(host, "ICMP ping", alias=host)
            queries2.append(q2)
            math2+=host+"+"
        title = "Users in " + group
        postfix = "/" + str(len(hosts))
        title2 = "Total Machines available in " + group
        myPanel = MathStatPanel(title=title, math=math[:-1], postfix=" user(s)", queryArray=queries)
        myPanel2 = MathStatPanel(title=title2, math=math2[:-1], postfix=postfix, queryArray=queries2)
        d.addPanels([myPanel, myPanel2])
    d.push()
main()
