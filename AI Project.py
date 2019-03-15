import snap
import snapPlot
import datetime
import time

"""
Following class deals with manipulating the snap graph, It has methods to threshold and cycle through
each node in the graph
"""

class snapGraph(object):

    #Constructor
    def __init__(self, network):
        self.network = network

    #Cycles through each node in the snap graph and displays its information
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
    This function takes in a minimum date and a maximum date, then thresholds the network based on those dates. If no
    maximum date is provided then the default is the first day of 2019, as no edges should have a time above this value
    The function takes the date in the form of a string, where the string has a pattern of DD.MM.YYYY, such as 17.03.2018
    would relate to the 17th of March 2018
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

    #Return the graph
    def returnNetwork(self):
        return self.network


####reads the data.csv file and returns a network contained within it

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

    ##    print(source, target, rating, time)
        if not (g.IsNode(source)):
            g.AddNode(source)
        if not (g.IsNode(target)):
            g.AddNode(target)
        g.AddEdge(source, target)
        
        g.AddIntAttrDatE(g.GetEI(source, target).GetId(), rating, "rating")
        g.AddFltAttrDatE(g.GetEI(source, target).GetId(), time, "time")
    dataFile.close()
    return g






importedGraph = importGraph()

network = snapGraph(importedGraph)

#network.cycleThroughNodes()

network.thresholdNetwork('17.07.2015', '20.01.2016')


plot = snapPlot.plotNet(network)
plot.draw()

#Below here are the other types of plots you can plot
#plot.draw("spect")
#plot.draw("c")
#plot.draw("fr")
#plot.draw("sh")

