import networkx as nx
import matplotlib.pyplot as plt
import snap

"""
The following class converts a snap graph to a networkx graph so that we can use the networkx plotting methods
"""


class plotNet(object):

    #Constructor cycles through all the snap nodes and adds them to networkx
    def __init__(self, network):

        network = network.returnNetwork()

        new_net = nx.DiGraph()
        for NI in network.Nodes():

            ID = NI.GetId()
            new_net.add_node(ID)

        for EI in network.Edges():

            ID = EI.GetId()
            time = network.GetFltAttrDatE(ID, "time")
            score = network.GetIntAttrDatE(ID, "rating")

            new_net.add_edge(EI.GetSrcNId(), EI.GetDstNId(), weight=score)
            new_net.add_edge(EI.GetSrcNId(), EI.GetDstNId(), time=time)

        self.network = new_net

    #Returns the networkx graph
    def getNetworkx(self):

        return self.network

    #determines the algorithim that will be used to draw the graph, based on users choice
    def determineGraphType(self, type):

        if type == "sp":
            return nx.spring_layout(self.network)

        elif type == "spect":
            return nx.spectral_layout(self.network)

        elif type == "sh":
            return nx.shell_layout(self.network)

        elif type == "fr":
            return nx.fruchterman_reingold_layout(self.network)

        elif type == "c":
            return nx.circular_layout(self.network)


    #Draw the graph
    def draw(self, type="sp"):

        drawType = self.determineGraphType(type)
        plt.axis('off')
        nx.draw_networkx(self.network, pos=drawType, with_labels=False, node_size=35)
        plt.show()
