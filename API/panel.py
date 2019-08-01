"""
Herbie Rand
Summer 2019

The panel class works with the dashboard class as part of Swat's 
custom grafana API. Panels are the data displays that can be 
created in a dashboard. Currently supported types of panels:
    - GraphPanel
    - SingleStatPanel
"""

import json
import sys

colorDictionary = {"red":"#C4162A", "blue":"#1F60C4", "green":"#37872D", "yellow":"#E0B400", "orange":"#FA6400", "purple":"#440563", "baby blue":"#8AB8FF", "grey":"#757575"}

class Panel:
    def __init__(self, panelType, title="title", queryArray=None, JSON=None, absLink=None):
        """
        Parameters: panelType (required), optional title and queryArray. If json found,
            initializes panel from json data instead of other arguments.
            NOTE: This constructor should not be called directly. Initialize your panels from one of the supported panel type constructors.
        """
        if JSON!=None:
            print("Initializing panel from json...")
            self.dictionary = json.loads(JSON)
            self.title = self.dictionary["title"]
            self.type = self.dictionary["type"]
            #throw exception if panelType != self.type
            self.queries=[]
            for target in self.dictionary["targets"]:
                host = target["host"]["filter"]
                group = target["group"]["filter"]
                item = target["item"]["filter"]
                application = target["application"]["filter"]
                q = Query(host, item, group=group, application=application)
                self.queries.append(q)
            h = self.dictionary["gridPos"]["h"]
            w = self.dictionary["gridPos"]["w"]
            x = self.dictionary["gridPos"]["x"]
            y = self.dictionary["gridPos"]["y"]
            self.id = 0
            self.position = [x, y]
            self.size = [h, w]
            self.sizeSet = False
        if JSON==None:
            print("Initializing panel from arguments...")
            self.title = title
            print(".....", self.title)
            self.type = panelType
            self.queries = []
            self.dictionary = {}
            self.id = 0
            self.position = [0, 0]
            self.size = [8, 12]
            self.sizeSet = False
            if absLink!=None:
                self.links=[{"title":"Click to go", "type":"absolute", "url":absLink}]
            else:
                self.links=None
            if queryArray!=None:
                self.queries.extend(queryArray)

    def _readJSON(self, filename):
        """read json from file, return as dict"""
        jPanel = open(filename)
        panelStr = jPanel.read()
        jPanel.close()
        d = json.loads(panelStr)
        return d
    
    def getDictionary(self):
        """
        Returns: panel's dictionary (python, not json)
        """
        return self.dictionary

    def getType(self):
        """
        Returns: this panel's type
        """
        return self.type

    def getTitle(self):
        """
        Returns: this panel's title
        """
        return self.title

    def getQueries(self):
        """
        Returns: array of this panel's queries
        """
        return self.queries
    
    def setID(self, panelID):
        """
        Parameters: panelID (positive int)
        """
        self.id = panelID
        if "id" in self.dictionary:
            self.dictionary["id"] = self.id

    def getID(self):
        """
        Returns: this panel's id
        """
        return self.id

    def _setPosition(self, x, y):
        """
        Parameters: x and y value to set panel position in dashboard
        """
        self.position = [x, y]
        self.dictionary["gridPos"]["x"] = x
        self.dictionary["gridPos"]["y"] = y
    
    def getPosition(self):
        """
        Returns: list[x,y] of panel position in the dashboard
        """
        return self.position
    
    def getSize(self):
        """
        Returns: this panel's size [h, w]
        """
        return self.size

    def _setSize(self, h, w):
        """
        Parameters: height and width
        """
        if not(self.sizeSet):
            self.size = [h, w]
            self.dictionary["gridPos"]["h"] = h
            self.dictionary["gridPos"]["w"] = w
            self.sizeSet = True
        else:
            print("The size on this panel has already been set.")
            print("Height: %s, Width: %s" % (self.size[0], self.size[1]))

    def _sizeSet(self):
        """
        Returns: bool indicating whether the size has been set on this panel.
        """
        return self.sizeSet

    def containsItem(self, itemName):
        """
        Parameters: name of item
        Returns: bool, true if this panel contains itemName, else false
        """
        for query in self.queries:
            if query.getItem()==itemName:
                return True
        return False

    def containsHost(self, hostName):
        """
        Parameters: name of host
        Returns: bool, true if this panel contains hostName, else false
        """
        for query in self.queries:
            if query.getHost()==hostName:
                return True
        return False
    
    def addQueries(self, queryList):                                              
        """
        Parameters: list of query objects to be added to this panel
        """
        for query in queryList:
            #Throw exceptions when someone gives something that's not a query object
            targetDict = {}
            if query.getApplication()!=None:
                targetDict["application"] = {"filter": query.getApplication()}
            else:
                targetDict["application"] = {"filter": ""}
            targetDict["functions"] = [{
                "added": False,
                "def": {
                    "category": "Alias",
                    "defaultParams": [],
                    "name": "setAlias",
                    "params": [{
                        "name": "alias",
                        "type": "string"
                        }]
                    },
                "params": [query.getItem()],
                "text": "setAlias(" + query.getItem() + ")"
                }]
            print("about to check if there is an alias...")
            if query.getAlias()!=None:
                print("found an alias!")
                print("Alias: %s" % query.getAlias())
                targetDict["functions"][0]["params"] = [query.getAlias()]
                targetDict["functions"][0]["text"] = "setAlias(" + query.getAlias() + ")"
            targetDict["group"] = {"filter": query.getGroup()}
            targetDict["host"] = {"filter": query.getHost()}
            targetDict["item"] = {"filter": query.getItem()}
            targetDict["mode"] = 0
            targetDict["options"] = {"showDisabledItems": False, "skipEmptyValues": False}
            targetDict["refId"] = "A"
            targetDict["resultFormat"] = "time_series"
            targetDict["table"] = {"skipEmptyValues": False}
            if query.getMode()!=None:
                targetDict["mode"] = query.getMode()
            self.dictionary["targets"].append(targetDict)

class SingleStatPanel(Panel):

    def __init__(self, title="title", queryArray=None, valueMaps=None, rangeMaps=None, 
            fontSize="100%", prefix=None, postfix=None, colors=None, thresholds=None, units=None, JSON=None, 
            decimals=None, sparkline=None, colorBackground=None, colorValue=None, absLink=None):
        """
        Parameters: optional title and queryArray, title is 'title' by default, 
        initializing from json is optional, but will overwrite other arguments if set
            valueMaps: a dictionary that maps certain values to text in a singlestat panel. Example:
                
            rangeMaps: a dictionary that maps ranges of values to text in a singleStat panel. Example:

            fontSize: size of the main stat displayed (not postfix/prefix/title). Default is 100%
            colors: a list of colors that correspond to thresholds. For example, if you wanted to low values to be green, medium to be orange, and high values to be red, you'd give the list in this order (see example 1), and set thresholds equal to a string (see below). If you want your singlestat panel to be one color only, provide an array as seen in example 2. See colorBackground and colorValue for more coloring options.
                Example1: colors=["green", "orange", "red"]
                Example2: colors=3*["purple"]
            thresholds: a string to fill in the thresholds field in grafana. 
                Example: thresholds = "1, 2"
            units: one of the supported unit types in grafana. These units don't always match the names found in grafana's singlestat panel visualization. The units entered here should match what you'd see in the json's "format" key in a particular panel. For example, instead of setting units to equal 'seconds', do this:
                Example: units='s'
            JSON: provide a JSON if you have an existing singleStatPanel you want to use with this API.
            decimals: optionally setst the number of decimals shown. 
                Example: decimals=2
            sparkline: bool, set to True if you want to see sparklines on your singleStat panel
                Example: sparkline=True
            colorValue: bool, set to True if you want the value in your singleStat panel to change color in accordance with your colors list and threshold arguments.
                Example: colorValue=True
            colorBackground: bool, set to True if you want the background in your singleStat panel to change color in accordance with your colors list and threshold arguments. NOTE: if you set both colorValue and colorBackground to True, you won't be able to see the value! (The whole panel will be one color!)
                Example: colorBackground=True
            absLink: absolute link, a url to be redirected to upon clicking on the panel.
                Example: absLink=<another dashboard's URL>
            See singleStat panel examples for details.
        """
#        print("ssp title: ", title)
#        print("ssp units: ", units)
#        print("ssp sparkline: ", sparkline)
#        print("ssp JSON: ", JSON)
#        print("ssp fs: ", fontSize)
        Panel.__init__(self, "singlestat", title=title, queryArray=queryArray, JSON=JSON, absLink=absLink)
        if JSON==None:
            self._buildDictionary(valueMaps, rangeMaps, fontSize, prefix, postfix, colors, thresholds, units, decimals, sparkline, colorValue, colorBackground)

    def _buildDictionary(self, valueMaps, rangeMaps, fontSize, prefix, postfix, colors, thresholds, units, decimals, sparkline, colorValue, colorBackground):
        """
        Description: to be called by constructor, builds singlestat panel dictionary
        """
        singleStatDictionary = self._readJSON("singlestat.json")
        singleStatDictionary["title"] = self.title
        singleStatDictionary["valueFontSize"] = fontSize
        if self.links!=None:
            singleStatDictionary["links"] = self.links
        print(sparkline, type(sparkline))
        if sparkline:
            singleStatDictionary["sparkline"]["show"] = True
        print(units, type(units))
        if units!=None:
            singleStatDictionary["format"]=units
        if decimals!=None:
            # should be a number, like 1 or 2
            singleStatDictionary["decimals"]=decimals  
        if valueMaps!=None:
            #Perform check to make sure we have the right type of value here!
            singleStatDictionary["mappingType"]=1
            singleStatDictionary["valueMaps"]=valueMaps
        if rangeMaps!=None:
            #same as above
            singleStatDictionary["mappingType"]=2
            singleStatDictionary["rangeMaps"]=rangeMaps
        if prefix!=None:
            singleStatDictionary["prefix"]=prefix
        if postfix!=None:
            singleStatDictionary["postfix"]=postfix
        if colors!=None:
            colorArray = []
            for color in colors:
                colorArray.append(colorDictionary[color])
            singleStatDictionary["colors"] = colorArray
        if thresholds!=None:
            singleStatDictionary["thresholds"] = thresholds
        if colorBackground:
            singleStatDictionary["colorBackground"] = True
        else:
            singleStatDictionary["colorBackground"] = False
        if colorValue:
            singleStatDictionary["colorValue"] = True
        else:
            singleStatDictionary["colorValue"] = False
        self.dictionary = singleStatDictionary             
        if self.queries!=None:                        
            self.addQueries(self.queries)
        self.id = 0
        self.position = [0,0]
    
    def addValueMap(self, valueMaps):
        """
        Parameters: an array of dictionaries that makes up a value map
        Description: maps values in the singlestat panel according to given array of dictionaries
        """
        #perform check on the value map to make sure it is of the right type
        self.dictionary["valueMaps"]=valueMaps

class MathStatPanel(SingleStatPanel):

    def __init__(self, title="title", queryArray=None, valueMaps=None, rangeMaps=None,
            fontSize="100%", prefix=None, postfix=None, colors=None, thresholds=None, units=None, JSON=None,
            decimals=None, sparkline=None, colorBackground=None, colorValue=None, absLink=None, math=""):
        """
        Parameters: this class inherits from SingleStat, and shares many optional parameters. See singlestat for details.
            math: a string that performs an operation on the given items using aliases as variable names
        """
        #Create appropriate color/threshold dictionary here!
        thresholdMap=None
        if colors!=None and thresholds!=None:
            thresholdMap = self._getThresholdMap(colors, thresholds)
        SingleStatPanel.__init__(self, title=title, queryArray=queryArray, valueMaps=valueMaps, rangeMaps=rangeMaps,
                fontSize=fontSize, prefix=prefix, postfix=postfix, units=units, JSON=JSON, decimals=decimals,sparkline=sparkline, colorBackground=colorBackground, 
                colorValue=colorValue, absLink=absLink)
        if JSON==None:
            self._buildMapDictionary(thresholdMap, math)

    def _buildMapDictionary(self, thresholdMap, math):
        """
        Parameters: thresholdmap, mathematical operation to be performed on queries, using aliases as variable names
        """
        self.dictionary["type"] = "blackmirror1-singlestat-math-panel"
        self.dictionary["links"] = []
        if self.links!=None:
            self.dictionary["links"] = self.links
        self.type = "MathStatPanel"
        if math!=None:
            self.dictionary["math"] = math
        if thresholdMap!=None:
            self.dictionary["thresholds"] = thresholdMap

    def _getThresholdMap(self, colors, thresholds):
        """
        Parameters: colors array, thresholds string, both as required in SingleStatPanel constructor
        Returns: an array of colors and thresholds as supported by math stat panel
        """
        thresholds = thresholds.replace(" ", "")
        thresholds = thresholds.split(",")
        thresholdList = [0]
        for value in thresholds:
            thresholdList.append(int(value))

        thresholdMap = []
        if len(colors)<len(thresholds):
            #raise exception, not enough colors!
            print("You done goofed!")
        else:
            for i in range(len(thresholdList)):
                oneMapping = {"color":colorDictionary[colors[i]], "value":thresholdList[i]}
                thresholdMap.append(oneMapping)
                print("Threshold Map: %s" % (thresholdMap))
            return thresholdMap

class GraphPanel(Panel):

    def __init__(self, title="title", queryArray=None, yAxesLeftMinMax=None, JSON=None, absLink=None, units=None):
        """
        Parameters: optional title and queryArray, title is 'title' by default
            queries can be added later with "addQueries()"
            optional yAxesLeftMinMax=[0,800000000] sets hard min/max for all graphs
        """
        Panel.__init__(self, "graph", title=title, queryArray=queryArray, JSON=JSON, absLink=absLink)
        if JSON==None:
            self._buildDictionary(yAxesLeftMinMax, units)

    def _buildDictionary(self, yAxesLeftMinMax, units):
        """
        Description: to be called by constructor, builds graph dictionary
        """

        graphDictionary = self._readJSON("graphpanel.json")
        graphDictionary["title"] = self.title
        if self.links!=None:
            graphDictionary["links"] = self.links
        if units != None:
            graphDictionary["yaxes"][0]["format"] = units
            graphDictionary["yaxes"][1]["format"] = units
        if yAxesLeftMinMax != None:
            graphDictionary["yaxes"][0]["min"] = yAxesLeftMinMax[0]
            graphDictionary["yaxes"][0]["max"] = yAxesLeftMinMax[1]
                            
        self.dictionary = graphDictionary
        if self.queries!=None:
            self.addQueries(self.queries)
        self.id = 0
        self.position = [0,0]

class Query:

    def __init__(self, host, item, group="/.*/", application=None, mode=None, alias=None):
        """
        Parameters: host name, item name, group and application name optional (group and application
            are optional filters that can be applied in grafana to help find the correct hosts/items,
            especially if there are duplicate host/item names)
            mode: number corresponding to the type of data displayed in your query. 
                Example: mode=0 (for metric queries)
                         mode=2 (for text queries)
        """
        self.host = host
        self.item = item
        self.group = group
        self.application = application
        self.mode = mode
        self.alias = alias

    def getHost(self):
        """
        Returns: host name for this query
        """
        return self.host
    
    def getItem(self):
        """
        Returns: item name for this query
        """
        return self.item

    def getGroup(self):
        """
        Returns: group name for this query
        """
        return self.group

    def getApplication(self):
        """
        Returns: application name for this query, may return 'None'
        """
        return self.application
    
    def getMode(self):
        """
        Returns: mode for this query's data
        """
        return self.mode
    
    def getAlias(self):
        """
        Returns: alias for this query
        """
        return self.alias
