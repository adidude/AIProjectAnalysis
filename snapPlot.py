import networkx as nx
import matplotlib.pyplot as plt
import snap

class plotNet(object):

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

        print nx.info(new_net)

    def getNetworkx(self):

        return self.network

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



    def draw(self, type="sp"):

        drawType = self.determineGraphType(type)
        plt.axis('off')
        nx.draw_networkx(self.network, pos=drawType, with_labels=False, node_size=35)
        plt.show()
"""
    def drawSpect(self):

        sp = nx.spectral_layout(self.network)
        plt.axis('off')
        nx.draw_networkx(self.network, pos=sp, with_labels=False, node_size=15)
        plt.show()

    def drawSH(self):

        sh = nx.shell_layout(self.network)
        plt.axis('off')
        nx.draw_networkx(self.network, pos=sh, with_labels=False, node_size=15)
        plt.show()

    def drawC(self):

        c = nx.circular_layout(self.network)
        plt.axis('off')
        nx.draw_networkx(self.network, pos=c, with_labels=False, node_size=15)
        plt.show()

    def drawFR(self):

        fr = nx.fruchterman_reingold_layout(self.network)
        plt.axis('off')
        nx.draw_networkx(self.network, pos=fr, with_labels=False, node_size=15)
        plt.show()
"""
