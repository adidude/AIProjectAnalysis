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

    """
    Uses the networkx draw functionality to draw the graph, node colour and drawing
    algorithim can be determined by the user by passing in the appropriate parameter: see below
    type : param the drawing algorithim used to draw the graph, default is sp but acceptable parameters are:
    sp, spect, sh, fr, c. Should be taken in as a string
    colourNodes : param a dictionary of keys pointing to a list of node Ids, make sure the key is the
    name of the colour that you want your nodes to come out as e.g. { "red" :: [12, 567, 548, 34] }
    colourEdges : param same as above, not been tested yet tho so don't use it
    """
    def draw(self, type="sp", colourNodes=None, colourEdges=None):

        drawType = self.determineGraphType(type)
        plt.axis('off')

        edgeMap = []
        nodeMap = []

        if not colourNodes:
            nodeMap = 'red'

        else:

            for node in self.network:
                for keys in colourNodes:

                    if node in colourNodes[keys]:
                        colour = keys
                        nodeMap.append(colour)

                    else:
                        nodeMap.append('red')

        if not colourEdges:
            edgeMap = 'black'

        else:

            for edge in self.network:
                for key, values in colourEdges:

                    if edge in values:
                        colour = key
                        edgeMap.append(colour)

                    else:
                        edgeMap.append('black')

        nx.draw_networkx(self.network, node_color=nodeMap, edge_colour= edgeMap, pos=drawType, with_labels=False, node_size=35, alpha=0.7)

        plt.show()






































"""        else:
            if colourNodes is not None:
                for i in colourNodes:
                    colour = self.getColour(i)
                    nx.draw_networkx_nodes(self.network, pos=drawType,
                                           nodelist=colourNodes[i],
                                           node_color=colour,
                                           node_size=35)

            for node in self.network:
                if node not in colourNodes:

                    nx.draw_networkx_nodes(self.network, pos=drawType,
                                           node_color='r',
                                           node_size=35)

            if colourEdges is not None:
                for i in colourEdges:

                    nx.draw_networkx_edges(G, pos,
                                           edgelist=[(0, 1), (1, 2), (2, 3), (3, 0)],
                                           width=2, edge_color=colour)"""
