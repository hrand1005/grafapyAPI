#!/usr/bin/python3
"""
Herbie Rand

This is a class for a grafana Dasbhoard, created as part of our custom grafana API.
"""

import json
import requests
from panel import Panel, GraphPanel, Query

class DashBoard:
    #add panels per row option
    def __init__(self, title="title", uid=None, token=None, url=None, JSON=None, panelsPerRow=2, panelHeight=8):
        """
        Parameters: title, uid, authentication token, url, JSON, panelsPerRow, and panelHeight.
            If a uid is set, a dashboard will be initialized using provided token and url by
            retrieving an existing dashboard. uid, token, and url must all be set to do this!
            If no uid is set, a new dashboard will be created with the optionally set title and
            other parameters.
            title:
                Title for the created dashboard. If not set, defaults to "title"
            uid:
                use this in conjunction with token and url to create a dashboard object from an existing grafana dashboard.
            token:
                Necessary authentication to push dashboards to grafana. See grafana documentation for details
            url:
                This should be the url of the dasbhoard you wish to modify. NOTE: do not include uid in this url, only everything up to the uid of the dashboard you wish to modify.
            JSON:
                Use this option to load in a dashboard from a JSON file. NOTE: Not all types of panels are supported in this API, so panel objects may not be initialized correctly. 
            panelsPerRow:
                Sets the number of panels you want to see per row in your dashboard. Ensures all supported panels are of uniform length.
            panelHeight:
                Sets the height of each panel in your dashboard. Ensures all supported panels are of uniform height.

        """
        self.title = title
        self.uid = uid
        self.headers = {"Accept": "application/json",
                        "Content-Type": "application/json",
                        "Authorization": "Bearer %s" % token}
        self.URL = url
        self.panels = []
        self.panelsPerRow = panelsPerRow
        self.panelHeight = panelHeight

        if (self.uid!=None):
            self._initWithUID()
        elif JSON!=None:
            self._importJSON(JSON)
        else:
            self._createNewDashBoard()

    def _initWithUID(self):
        """
        Description: private method to be called by constructor to initialize dashboard object with json
            from grafana
        """
        if (self.URL==None):
            raise Exception("You must set url to initialize DashBoard with UID.")

        urlPlusUID = self.URL + self.uid 
        dashObj = requests.get(urlPlusUID, headers=self.headers)

        if dashObj.status_code!=200:
            raise Exception("Dashboard not found. \nStatus code %s \nURL: %s " % (dashObj.status_code,urlPlusUID))
        self._importJSON(dashObj.text)
    
    def _importJSON(self, dashObj):
        """
        Parameters: json string of a grafana dashboard
        Description: private method to be called when importing json or initializing dashboard from uid
        """
        self.dictionary = json.loads(dashObj)
        self.title = self.dictionary["dashboard"]["title"]
        for panel in self.dictionary["dashboard"]["panels"]:
            #for now, only initializing graph and singlestat type panels
            if panel["type"]=="graph":
                pan = GraphPanel(JSON=json.dumps(panel))
            else:
                pan = SingleStatPanel(JSON=json.dumps(panel))
            self.panels.append(pan)
    
    def _createNewDashBoard(self):
        """
        Description: private method to be called by constructor to create a new dashboard dictionary
        """
        print("Creating new dashboard '%s'" % self.title)
        dashContents = {"id": None,
                        "title": self.title,
                        "tags": [],
                        "panels": [],
                        "timezone": "browser",
                        "rows": [{}],
                        "schemaVersion": 16,
                        "version": 0}
        self.dictionary = {"dashboard":dashContents, "folderID":0, "overwrite":False}
        self.uid = "unknown"

    def addPanels(self, panelArray):
        """
        Parameters: a list of panels
        Description: adds and sorts panel objects to this dashboard. Supported panels: Graph Panels, SingleStat Panels. Using addPanels sorts panels by assigning them ids from 0 to (number of panels - 1), and adds panels in in uniform size one row at a time, left to right.
        """
        if len(self.panels)!=0:
            for panel in self.panels:
                if panel.getID()>=len(self.panels):
                    self.panels = self._sortPanels(self.panels, 0)
        panelArray = self._sortPanels(panelArray, len(self.panels))
        self.panels.extend(panelArray)
        for panel in panelArray:
            self.dictionary["dashboard"]["panels"].append(panel.getDictionary())
    
    def _sortPanels(self, panelArray, startID):
        """
        Parameters: array of panels to be properly ID'd and positioned
        Returns: Updated array
        """
        for i in range(len(panelArray)):
            panelArray[i].setID(i+startID)
            panelArray[i].setSize(self.panelHeight, 24/self.panelsPerRow)
            if (i+startID)-self.panelsPerRow<0:
                x = (i+startID)*(24/self.panelsPerRow)
                y = 0
            else:
                x = ((i+startID)%(self.panelsPerRow))*(24/self.panelsPerRow)
                y = (i+startID)/self.panelsPerRow * self.panelHeight
            panelArray[i].setPosition(x, y)
        return panelArray

    def getPanels(self):
        """
        Returns: list of supported panels contained within this dashboard
        """
        return self.panels

    def removePanelsByHost(self, hostNameArray):
        """
        Parameters: list of host names to be checked with this dashboard's panels. Panels with the host
            will be removed from the dashboard. 
        """
        sort = False
        for host in hostNameArray:
            changed = self._removePanelBy("host", host)
            if changed:
                sort = True
        if sort:
            self._sortPanels(self.panels, 0)
        else:
            print("No panels with those hosts found in your dashboard!")
    
    def removePanelsByItem(self, itemNameArray):
        """
        Parameters: list of item names to be checked with this dashboard's panels. Panels with the item
            will be removed from the dashboard.
        """
        sort = False
        for item in itemNameArray:
            changed = self._removePanelBy("item", item)
            if changed:
                sort = True
        if sort:
            self._sortPanels(self.panels, 0)
        else:
            print("No panels with those items found in your dashboard!")
    
    def removePanelsByTitle(self, titleArray):
        """
        Parameters: list of title names to be checked with this dashboard's panels. Panels with matching title
            will be removed from the dashboard.
        """
        sort = False
        for title in titleArray:
            changed = self._removePanelBy("title", title)
            if changed:
                sort = True
        if sort:
            self._sortPanels(self.panels, 0)
        else:
            print("No panels with those titles found in your dashboard!")
    
    def _removePanelBy(self, key, value):
        """
        Parameters: key and value of what should be removed from the dashboard dictionary
        Returns: bool indicating whether a change was made to the dictionary
        Description: private method called by 'removePanelsBy...' methods
        """
        toRemove = []
        found = False
        changed = False
        for panel in self.panels:
            if key!="title":
                if key=="host":
                    if panel.containsHost(value):
                        toRemove.append(panel)
                        changed = True
                        found = True
                    else:
                        found = False
                elif key=="item":
                    if panel.containsItem(value):
                        toRemove.append(panel)
                        changed = True
                        found = True
                    else:
                        found = False
                else:
                    print("Unrecognized key '%s'" % (key))
                    raise Exception("You broke the API!")
                if found:
                    for panel in self.dictionary["dashboard"]["panels"]:
                        for target in panel["targets"]:
                            if target[key]["filter"]==value:
                                print(panel["title"] + " removed from dashboard.")
                                self.dictionary["dashboard"]["panels"].remove(panel)
                                changed = True
                                found = False
            else:
                if panel.getTitle()==value:
                    toRemove.append(panel)
                    changed = True
                    for panel in self.dictionary["dashboard"]["panels"]:
                        if panel["title"]==value:
                            print(value + "removed from dashbaord.")
                            self.dictionary["dashboard"]["panels"].remove(panel)
                            changed = True 
        for panel in toRemove:
            self.panels.remove(panel)
        return changed 

    def __str__(self):
        """
        Returns: A string containing the following with line formatting:
            title: 
            uid: 
            url: 
            panels: 
            panels per row: 
            panel height:

        """
        dbString = "title: %s\nuid: %s\nurl: %s\npanels: " % (self.title, self.uid, self.URL)
        dbString += "%s" % len(self.panels)
        dbString += "\npanels per row: %s\npanel height: %s" % (self.panelsPerRow, self.panelHeight)
        return dbString

    def push(self, postURL=None):
        """
        Description: pushes the dashboard object to grafana, if there is an existing dashboard with 
            the same uid, it will be overwritten
        """
        if postURL==None:
            postURL=self.URL
        if postURL==None:
            raise Exception("No postURL set! Either provide a url in the constructor or set postURL=<url> in this method.")
        self.dictionary["overwrite"] = True
        response = requests.post(postURL, headers=self.headers, json=self.dictionary)
        if(response.status_code!=200):
            raise Exception("DashBoard could not be posted to %s. Status code: %s" % (postURL, response.status_code))
        else:
            print("%s successfully posted." % (self.title))
        return response

    def rename(self, title):
        """
        Parameters: title to replace current title
        """
        self.title = title
        self.dictionary["dashboard"]["title"] = self.title
    
    def exportToJSON(self):
        """
        Returns: string in json format of this dashboard.
        """
        return json.dumps(self.dictionary)
 
####################################################################

def main():
    """simple test code here"""
    token = None
    url = None
    db = DashBoard("simpleTestdb", None, token, url)

if __name__ == "__main__":
    main()
