import snap
import snapPlot
import datetime
import time

class snapGraph(object):

    #Constructor
    def __init__(self, network):
        self.network = network

    #Cycles through each node in the snap graph and displays its information
    def cycleThroughNodes(self):


        print("Nodes: " + str(self.network.GetNodes()) + "\t" + "Edges: " + str(self.network.GetEdges()) + "\n")
        for edge in self.network.Edges():
            n.draw("file.png")
            print("Edge ID: " + str(edge.GetId()))
            print("Source Node: " + str(edge.GetSrcNId()) + " --> Target Node: " + str(edge.GetDstNId()))
            print("Rating: " + str(self.network.GetIntAttrDatE(edge.GetId(), "rating")))

            #convert date to epoch time using the datetime python library
            ts_epoch = self.network.GetFltAttrDatE(edge.GetId(), "time")
            print("Time: " + datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d'))
            time.sleep(1)


    """This function takes in a minimum date and a maximum date, then thresholds the network based on those dates. If no
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

    # Calculates betweens centrality for each node and stores it inside the node as attribute "bcentrality2".
    # Draws a graph of different coloured nodes.
    def betweenCentral(self,name, date, nodeColour, nodeSize):

            temp = self.network
            temp.AddFltAttrN("bcentrality")

            # Colour Hash Table
            NIdColorH = snap.TIntStrH()
            red = 0
            orange = 0
            yellow = 0
            green = 0
            blue = 0

            # For every node
            for NI in temp.Nodes():

                # Get ITs betweenes centrality
                CloseCentr = snap.GetClosenessCentr(temp, NI.GetId())
                temp.AddFltAttrDatN(NI.GetId(),CloseCentr,"bcentrality")

                # Determine colour
                if CloseCentr <0.2:
                    NIdColorH[NI.GetId()] = "red"
                    red+=1
                    nodeColour.append("red")
                    nodeSize.append(30)

                elif CloseCentr <0.4:
                    NIdColorH[NI.GetId()] = "orange"
                    orange+=1
                    nodeColour.append("orange")
                    nodeSize.append(40)

                elif CloseCentr <0.6:
                    NIdColorH[NI.GetId()] = "yellow"
                    yellow+=1
                    nodeColour.append("yellow")
                    nodeSize.append(50)

                elif CloseCentr <0.8:
                    NIdColorH[NI.GetId()] = "green"
                    green+=1
                    nodeColour.append("green")
                    nodeSize.append(60)

                else:
                    NIdColorH[NI.GetId()] = "blue"
                    blue+=1
                    nodeColour.append("blue")
                    nodeSize.append(70)


            print"Red:\t", red
            print"Orange:\t" , orange
            print"Yellow:\t", yellow
            print"Green:", green
            print"blue:\t" ,blue

            # Draw graph
            snap.DrawGViz(temp, snap.gvlSfdp, name +".png", date, True, NIdColorH)



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


####reads the data.csv file and returns a network contained within it

def importGraph():
    dataFile = open("data.csv", "r")
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

nodeColour = []
nodeSize = []

importedGraph = importGraph()

#How to make a new snap graph class
network = snapGraph(importedGraph)
network.thresholdNetwork('08.11.2013', '20.01.2014')
network.betweenCentral( "Rise","08.11.2013 20.01.2014",nodeColour,nodeSize)
plot = snapPlot.plotNet(network)
plot.draw(colourNodes=nodeColour,nodeSize=35)


"""
network = snapGraph(importedGraph)
network.thresholdNetwork('20.01.2014', '07.04.2014')
network.betweenCentral("Fall","20.01.2014 - 07.04.2014",nodeColour,nodeSize)
plot = snapPlot.plotNet(network)
plot.draw(colourNodes=nodeColour,nodeSize=35)
"""
