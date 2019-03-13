import snap
import snapPlot
import time as timetime

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



graph = importGraph()

plot = snapPlot.plotNet(graph)
plot.plotGraph()



"""
labels = snap.TIntStrH()
for NI in graph.Nodes():
    labels[NI.GetId()] = str(NI.GetId())
snap.DrawGViz(graph, snap.gvlDot, "output.png", " ", labels)
"""


"""
print("Nodes: " + str(graph.GetNodes()) + "\t" + "Edges: " + str(graph.GetEdges()) + "\n")
for edge in graph.Edges():
    print("Edge ID: " + str(edge.GetId()))
    print("Source Node: " + str(edge.GetSrcNId()) + " --> Target Node: " + str(edge.GetDstNId()))
    print("Rating: " + str(graph.GetIntAttrDatE(edge.GetId(), "rating")))
    print("Time: " + str(graph.GetFltAttrDatE(edge.GetId(), "time")))
    print
    timetime.sleep(1)
"""


####creates a .dot file that idk what to do with
##snap.DrawGViz(graph, snap.gvlDot, "graph.png", "graph")


####if gnuplot is installed, creates a .plt file that when run creates a plot png
#snap.PlotInDegDistr(graph, "Plot", "Descriptiom of the plot")
