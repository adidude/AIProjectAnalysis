import snap
import networkx as nx
import matplotlib.pyplot as plt

import time as timetime

####reads the data.csv file and returns a network contained within it

def importGraph():
    dataFile = open("data.csv", "r")
    #g = snap.TNEANet.New()
    g = nx.Graph()
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
        if not (g.has_node(source)):
            g.add_node(source)
        if not (g.has_node(target)):
            g.add_node(target)
        g.add_edge(source, target, weight=rating, time=time)
        
        #g.AddIntAttrDatE(g.GetEI(source, target).GetId(), rating, "rating")
        #g.AddFltAttrDatE(g.GetEI(source, target).GetId(), time, "time")
    dataFile.close()
    return g



graph = importGraph()

print nx.info(graph)

sp=nx.spring_layout(graph)

plt.axis('off')

nx.draw_networkx(graph, pos=sp, with_labels=False, node_size=35)

plt.show()


"""
print("Nodes: " + str(graph.GetNodes()) + "\t" + "Edges: " + str(graph.GetEdges()) + "\n")
for edge in graph.Edges():
    print("Edge ID: " + str(edge.GetId()))
    print("Source Node: " + str(edge.GetSrcNId()) + " --> Target Node: " + str(edge.GetDstNId()))
    print("Rating: " + str(graph.GetIntAttrDatE(edge.GetId(), "rating")))
    print("Time: " + str(graph.GetFltAttrDatE(edge.GetId(), "time")))
    print
    timetime.sleep(1)


####creates a .dot file that idk what to do with
##snap.DrawGViz(graph, snap.gvlDot, "graph.png", "graph")


####if gnuplot is installed, creates a .plt file that when run creates a plot png
snap.PlotInDegDistr(graph, "Plot", "Descriptiom of the plot")
"""