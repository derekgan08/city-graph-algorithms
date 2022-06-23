import networkx as nx
import networkx.exception
import matplotlib.pyplot as plt
import random
import os


vertex_list = [
    {"label": "LA", "fullname": "Los Angeles", "pos": (1, 4)},
    {"label": "BL", "fullname": "Berlin", "pos": (5, 6)},
    {"label": "SB", "fullname": "Salzburg", "pos": (6, 5)},
    {"label": "RM", "fullname": "Rome", "pos": (5, 3)},
    {"label": "MV", "fullname": "Montevideo", "pos": (2, 1)},
]


class Graph:
    # Constructor to initialize the graph
    def __init__(self):
        distance_BL_LA = 9310
        distance_BL_SB = 526
        distance_SB_RM = 659
        distance_RM_MV = 11032
        distance_MV_LA = 10020

        self.graph = nx.DiGraph()
        self.graph.add_nodes_from([
            (vertex_list[0]["label"], {"pos": vertex_list[0]["pos"]}),
            (vertex_list[1]["label"], {"pos": vertex_list[1]["pos"]}),
            (vertex_list[2]["label"], {"pos": vertex_list[2]["pos"]}),
            (vertex_list[3]["label"], {"pos": vertex_list[3]["pos"]}),
            (vertex_list[4]["label"], {"pos": vertex_list[4]["pos"]}),
        ])

        self.graph.add_weighted_edges_from([
            (vertex_list[1]["label"], vertex_list[0]["label"], distance_BL_LA),
            (vertex_list[1]["label"], vertex_list[2]["label"], distance_BL_SB),
            (vertex_list[2]["label"], vertex_list[3]["label"], distance_SB_RM),
            (vertex_list[3]["label"], vertex_list[4]["label"], distance_RM_MV),
            (vertex_list[4]["label"], vertex_list[0]["label"], distance_MV_LA)
        ])

    # Reset the graph by reinitializing the graph
    def reset_graph(self, print_graph=False):
        self.__init__()

        if print_graph:
            self.print_graph()

    # Add new edge enter by user
    def add_new_edge(self, v1, v2):
        self.graph.add_edge(v1, v2)
        self.print_graph(title="Graph with newly added edge")

    # Remove edge enter by user
    def remove_edge(self, v1, v2):
        try:
            self.graph.remove_edge(v1, v2)
            self.print_graph(title="Graph with removed edge")
        except networkx.exception.NetworkXError:
            print("This edge does not exist. It could be because this edge is not in the graph"
                  "\nOR"
                  "\nThe direction of the edge is wrong")
            
    '''
    Function to print the graph
    If there is no graph or subgraph provided, the program will print the graph available inside the Graph class
    else, it will print the graph or subgraph provided
    
    If curve is specified to be false, the graph produced will have a straight line curve, this is to cater for printing
    the spanning tree at function 4
    
    The function will also print the title of the graph if the title is given
    '''

    def print_graph(self, selected_graph=None, curve=True, title=None):
        plt.title(title)
        if selected_graph is None:
            pos = nx.get_node_attributes(self.graph, "pos")
            labels = nx.get_edge_attributes(self.graph, "weight")
            nx.draw(self.graph, pos, with_labels=True, font_weight='bold',
                    connectionstyle="arc3,rad=0.3" if curve else "arc3")
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels, font_size=7)
        else:
            pos = nx.get_node_attributes(selected_graph, "pos")
            labels = nx.get_edge_attributes(selected_graph, "weight")
            nx.draw_networkx(selected_graph, pos, with_labels=True, font_weight='bold',
                             connectionstyle="arc3,rad=0.3" if curve else "arc3")
            nx.draw_networkx_edge_labels(selected_graph, pos, edge_labels=labels, font_size=7)

        plt.show()

    # Print the adjacency list of the graph
    def print_adjacency_list(self):
        print("==================================")
        print("Adjacency List for graph, first column is the starting vertex, while the following columns are adjacent "
              "vertices")
        for line in nx.generate_adjlist(self.graph):
            print(line)

    # Check if the graph has a cycle, return True if a cycle is detected
    def has_cycle(self):
        return len(sorted(nx.simple_cycles(self.graph))) > 0