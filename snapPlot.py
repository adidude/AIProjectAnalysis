import networkx as nx
import matplotlib.pyplot as plt
import snap

class plotNet(object):

    def __init__(self, network):

        new_net = nx.Graph()
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

        #print nx.info(new_net)

    def plotGraph(self):

        sp = nx.spring_layout(self.network)

        plt.axis('off')

        nx.draw_networkx(self.network, pos=sp, with_labels=False, node_size=15, edge_size=1)

        plt.show()
