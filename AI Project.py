import snap
import snapPlot
import datetime
import time
#import statistics

"""
Following class deals with manipulating the snap graph, It has methods to threshold and cycle through
each node in the graph
"""

class snapGraph(object):

    #Constructor
    def __init__(self, network):
        self.network = network

    """Cycles through each node in the snap graph and displays its information"""
    def cycleThroughNodes(self):

        print("Nodes: " + str(self.network.GetNodes()) + "\t" + "Edges: " + str(self.network.GetEdges()) + "\n")
        for edge in self.network.Edges():

            print("Edge ID: " + str(edge.GetId()))
            print("Source Node: " + str(edge.GetSrcNId()) + " --> Target Node: " + str(edge.GetDstNId()))
            print("Rating: " + str(self.network.GetIntAttrDatE(edge.GetId(), "rating")))

            #convert date to epoch time using the datetime python library
            ts_epoch = self.network.GetFltAttrDatE(edge.GetId(), "time")
            print("Time: " + datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d'))
            time.sleep(1)

    """
    Method makes a deep copy of the network and returns it
    copy :return: the deep copy of the network
    """
    def deepCopy(self):

        copy = snap.TNEANet.New()

        for NI in self.network.Nodes():

            copy.AddNode(NI.GetId())

        for EI in self.network.Edges():

            source = EI.GetSrcNId()
            target = EI.GetDstNId()
            time = self.network.GetFltAttrDatE(EI, "time")
            score = self.network.GetIntAttrDatE(EI, "rating")

            copy.AddEdge(source, target)
            copy.AddIntAttrDatE(EI.GetId(), score, "rating")
            copy.AddFltAttrDatE(EI.GetId(), time, "time")

        return copy

    """
    This function takes in a minimum date and a maximum date, then thresholds the network based on those dates. If no
    maximum date is provided then the default is the first day of 2019, as no edges should have a time above this value
    The function takes the date in the form of a string, where the string has a pattern of DD.MM.YYYY, such as 17.03.2018
    would relate to the 17th of March 2018
    min : param minimum date to be used as  threshold, taken in as a string in the form DD.MM.YYYY
    max : param maximum date to be used as  threshold, taken in as a string in the form DD.MM.YYYY, default is 01.01.2019
    """
    def thresholdNetwork(self, min, max='01.01.2019'):

        import time
        pattern = '%d.%m.%Y'

        minEpoch = time.mktime(time.strptime(min, pattern))
        maxEpoch = time.mktime(time.strptime(max, pattern))

        #Removes edges not within the time frame
        for EI in self.network.Edges():
            time = self.network.GetFltAttrDatE(EI, "time")
            if time < minEpoch or time > maxEpoch:
                self.network.DelEdge(EI.GetSrcNId(), EI.GetDstNId())

        #Removes Nodes with No Edges
        for NI in self.network.Nodes():
            if NI.GetInDeg() == 0 and NI.GetOutDeg() == 0:
                self.network.DelNode(NI.GetId())

    #returns the network
    def returnNetwork(self):
        return self.network

    #Will draw a graph that shows the correlation between the degree/number of incoming and outgoing edges.
    #Closeness centrality can be plotted.
    def degreeCorrelation(self):
        #Opens degreecorrelation data file or creates it.
        compiledGraph = open("DegreeCorrelation.dat","w+")
        #For each node
        for node in self.network.Nodes():
            #Get's its inward and outward degree
            outDeg = node.GetOutDeg()
            inDeg = node.GetInDeg()
            #saves the degrees as coordinates.
            self.saveCoordinates(outDeg,inDeg,compiledGraph,True)
            #self.saveCoordinates(outDeg,compiledGraph,False)

    def centralityCorrelation(self):
        #Opens cntrltyCrltn data file or creates it.
        #print("centrality noting started\n")
        compiledGraph = open("cntrltyCrltn.dat","w+")
        #stores all centralities.
        #print("Entering centrality method\n")


        #Will act as iterator
        i=0
        #print("Entering centralityCorrelation for loop\n")
        #For each node
        for node in self.network.Nodes():
            #Get's its inward and outward degree
            outDeg = node.GetOutDeg()
            inDeg = node.GetInDeg()
            CloseCentr = snap.GetClosenessCentr(self.network, node.GetId())
            #saves the degrees as coordinates.
            self.saveCoordinates(outDeg,inDeg,compiledGraph,False,CloseCentr)
            #self.saveCoordinates(outDeg,inDeg,compiledGraph,True)
            #self.saveCoordinates(outDeg,compiledGraph,False)
            i+=1

    """
    def betweeenessCorrelation(self):
        #Opens cntrltyCrltn data file or creates it.
        #print("centrality noting started\n")
        compiledGraph = open("btwnsCrltn.dat","w+")
        #stores all centralities.
        #print("Entering centrality method\n")

        #Will act as iterator
        i=0
        #print("Entering centralityCorrelation for loop\n")
        #For each node
        for node in self.network.Nodes():
            #Get's its inward and outward degree
            outDeg = node.GetOutDeg()
            inDeg = node.GetInDeg()
            #saves the degrees as coordinates.
            self.saveCoordinates(outDeg,inDeg,compiledGraph,True,centralities[i])
            #self.saveCoordinates(outDeg,inDeg,compiledGraph,True)
            #self.saveCoordinates(outDeg,compiledGraph,False)
            i+=1
    """

    """
    finds the number of nodes with highest degrees as specified by the user
    search : parameter the number of nodes to be found and returned
    degrees :return: A list of node ID's that have the highest degree in the graph
    """
    def findHighestDegrees(self, search=1):

        copy = self.deepCopy()
        degrees = []
        for i in range(0, search):
            degrees.append(snap.GetMxDegNId(copy))
            copy.DelNode(degrees[i])
        return degrees
    """
    finds the number of nodes with highest strengths as specified by the user
    search : parameter the number of nodes to be found and returned
    degrees :return: A dictionary of node ID's that have the highest strength in the graph
    """
    def findHighestStrength(self, search=1):

        highestStrengths= []
        nodeStrengths = {}

        for EI in self.network.Edges():

            node = EI.GetDstNId()

            if node in nodeStrengths:

                strength = nodeStrengths[node]
                strength = strength + self.network.GetIntAttrDatE(EI, "rating")
                nodeStrengths[node] = strength

            else:
                nodeStrengths[node] = self.network.GetIntAttrDatE(EI, "rating")

        for i in range(0, search):

            max = maxkey = 0

            for keys in nodeStrengths:
                if max < nodeStrengths[keys]:
                    max = nodeStrengths[keys]
                    maxkey = keys

            highestStrengths.append(maxkey)
            del nodeStrengths[maxkey]

        return highestStrengths
    """
    finds the average of all the ratings
    """
    def averageRating(self):

        ratingSum = 0

        for EI in self.network.Edges():
            ratingSum += self.network.GetIntAttrDatE(EI, "rating")

        return float(ratingSum) / float(self.network.GetEdges())
    """
    converts the positive ratings to 10 and negative to -10
    """
    def binarize(self):

        for EI in self.network.Edges():

            if(self.network.GetIntAttrDatE(EI, "rating") > 0):
                self.network.DelAttrDatE(EI.GetId(), "rating")
                self.network.AddIntAttrDatE(EI.GetId(), 10, "rating")
            if(self.network.GetIntAttrDatE(EI, "rating") < 0):
                self.network.DelAttrDatE(EI.GetId(), "rating")
                self.network.AddIntAttrDatE(EI.GetId(), -10, "rating")
    """
    calculates the closeness centralities and stores them in a list
    list : return : list of closeness centralities
    """
    def getClosenessCentralities(self):
        centralities = []
        #print("In closeness method")
        for NI in self.network.Nodes():
            #print("Selected new origin node.\n")
            sumShortestPaths = 0

            for NI2 in self.network.Nodes():
                #print("Selected new comparitive node\n")
                sumShortestPaths += abs(snap.GetShortPath(self.network, NI.GetId(), NI2.GetId()))

            closeness = float(sumShortestPaths) / float(self.network.GetNodes())
            centralities.append(closeness)
        #print("Finished getting centrality values\n")
        return centralities


    # Calculates betweens centrality for each node and stores it inside the node as attribute "bcentrality2".
    # Draws a graph of different coloured nodes.
    def betweenCentral(self,date):

            temp = self.network
            temp.AddFltAttrN("bcentrality")

            # Colour Hash Table
            NIdColorH = snap.TIntStrH()
            purple = 0
            blue = 0
            green = 0
            yellow = 0
            red = 0
            # For every node
            for NI in temp.Nodes():

                # Get ITs betweenes centrality
                CloseCentr = snap.GetClosenessCentr(temp, NI.GetId())
                temp.AddFltAttrDatN(NI.GetId(),CloseCentr,"bcentrality")

                # Determine colour
                if CloseCentr <0.2:
                    NIdColorH[NI.GetId()] = "purple"
                    purple+=1

                elif CloseCentr <0.4:
                    NIdColorH[NI.GetId()] = "blue"
                    blue+=1

                elif CloseCentr <0.6:
                    NIdColorH[NI.GetId()] = "green"
                    green+=1

                elif CloseCentr <0.8:
                    NIdColorH[NI.GetId()] = "yellow"
                    yellow+=1

                else:
                    NIdColorH[NI.GetId()] = "red"
                    red+=1

            print"Purple:\t", purple
            print"Blue:\t" , blue
            print"Green:\t", green
            print"Yellow:", yellow
            print"Red:\t" ,red

            # Draw graph
            #snap.DrawGViz(temp, snap.gvlSfdp, "BetweenesCentrality.png", date, True, NIdColorH)


            """
                Nodes = snap.TIntFltH()
                Edges = snap.TIntPrFltH()
                snap.GetBetweennessCentr(graph, Nodes, Edges, 1.0)

                for node in Nodes:
                    temp.AddIntAttrDatN(node,Nodes[node],"bcentrality")

                for edge in Edges:
                    print "edge: (%d, %d) centrality: %f" % (edge.GetVal1(), edge.GetVal2(), Edges[edge])

                return temp
            """

    #Will save the input coordinates to a file.
    def saveCoordinates(self,x,y,file,isWithLine,centrality=0):
        #file.write("{}\t{}\t{}\n".format(x,y,centrality))
        file.write("{}\t{}\n".format(centrality,y))
        #file.write("{}\t{}\n".format(y,centrality))
        if isWithLine:
            pass
        else:
            file.write("\n")


"""
opens the data file and converts it into a SNAP network
g : return : SNAP network graph
"""
def importGraph():

    dataFile = open("soc-sign-bitcoinotc.csv", "r")
    g = snap.TNEANet.New()

    while True:

        data = dataFile.readline().split(",")
        data[len(data) - 1] = data[len(data) - 1].replace("\n", "")
        if(data == ['']):
            break

        source = int(data[0])
        target = int(data[1])
        rating = int(data[2])
        time = float(data[3])

        if not (g.IsNode(source)):
            g.AddNode(source)
        if not (g.IsNode(target)):
            g.AddNode(target)
        g.AddEdge(source, target)

        g.AddIntAttrDatE(g.GetEI(source, target).GetId(), rating, "rating")
        g.AddFltAttrDatE(g.GetEI(source, target).GetId(), time, "time")

    dataFile.close()
    return g

"""
Takes in two lists, and if there is any overlap, will return a list of 3 lists, the last list containing the overlapping
elements that have been removed from the first two lists
list1 : param The first list to be checked
list2 : param The second list to be checked
listolist :return: the three lists
"""
def findOverlap(list1, list2):

    listolist = []
    list3 = []
    found = False

    for item in list1:
        if item in list2:
            list3.append(item)
            found = True

    listolist.append(list1)
    listolist.append(list2)
    listolist.append(list3)

    if found:
        return listolist
    else:
        return found

importedGraph = importGraph()

#How to make a new snap graph class
network = snapGraph(importedGraph)

#Will draw a graph showing the relationship between inward and outward edges.
#network.degreeCorrelation()
network.centralityCorrelation()
"""
#How to threshold
network.thresholdNetwork('17.07.2015', '20.01.2016')

#find 5 highest degrees
degreeNodes = network.findHighestDegrees(5)

#fins 5 highest strengths
strengthNodes = network.findHighestStrength(5)

d1 = {}
#makes sure the key is the colour you want to be plotting
d1["blue"] = degreeNodes

d3 = {}

d3["purple"] = strengthNodes

#find common nodes
overlap = findOverlap(d1["blue"], d3["purple"])

d2 = {}

d2["yellow"] = overlap.pop()


print("average rating: " + str(network.averageRating()))

##print(network.getClosenessCentralities())

#how to binarize
network.binarize()

plot = snapPlot.plotNet(network)

#plot common nodes, highlighting those of interest
plot.draw(colourNodes=d1)

plot.draw(colourNodes=d2)
"""
#Below here are the other types of plots you can plot
#plot.draw("spect")
#plot.draw("c")
#plot.draw("fr")
#plot.draw("sh")
