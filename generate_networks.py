import networkx as nx
import matplotlib.pyplot as plt

def star(population):
    #network = {0 : [list(range(1, population))]}
    #for player in range(1, population):
    #    network[player] = [0]
    
    network = nx.Graph()
    network.add_nodes_from([1, population])
    for i in range(2, population+1):
        network.add_edge(1, i)
    return(network)

G = star(100)
nx.draw_shell(G)
plt.show()