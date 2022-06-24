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
    
    '''
    Add a random edge in the graph.
    It will also return the vertices where the random edge was added.
    
    This function will also work either a graph is provided or not.
    '''
    def add_random_edge(self, selected_graph=None):
        # Define the other edge's distance
        distance_LA_SB = 9704
        distance_LA_RM = 10190
        distance_BL_RM = 1184
        distance_BL_MV = 11817
        distance_SB_MV = 11477
        distance_LA_BL = 9310
        distance_SB_BL = 526
        distance_RM_SB = 659
        distance_MV_RM = 11032
        distance_LA_MV = 10020

        edge_distance = 0
        # Get the list of nodes that dose not have an edge, then randomly choose from there
        non_edges = list(nx.non_edges(self.graph if selected_graph is None else selected_graph))

        # Abort this function if there are already no empty available edges in the graph
        if len(non_edges) == 0:
            return

        # Compute the edge distance based on the vertex combination
        chosen_edge = list(random.choice(non_edges))
        if (chosen_edge[0] == "LA" or chosen_edge[1] == "LA") and (chosen_edge[0] == "SB" or chosen_edge[1] == "SB"):
            edge_distance = distance_LA_SB
        elif (chosen_edge[0] == "LA" or chosen_edge[1] == "LA") and (chosen_edge[0] == "RM" or chosen_edge[1] == "RM"):
            edge_distance = distance_LA_RM
        elif (chosen_edge[0] == "BL" or chosen_edge[1] == "BL") and (chosen_edge[0] == "RM" or chosen_edge[1] == "RM"):
            edge_distance = distance_BL_RM
        elif (chosen_edge[0] == "BL" or chosen_edge[1] == "BL") and (chosen_edge[0] == "MV" or chosen_edge[1] == "MV"):
            edge_distance = distance_BL_MV
        elif (chosen_edge[0] == "SB" or chosen_edge[1] == "SB") and (chosen_edge[0] == "MV" or chosen_edge[1] == "MV"):
            edge_distance = distance_SB_MV
        elif (chosen_edge[0] == "LA" or chosen_edge[1] == "LA") and (chosen_edge[0] == "BL" or chosen_edge[1] == "BL"):
            edge_distance = distance_LA_BL
        elif (chosen_edge[0] == "SB" or chosen_edge[1] == "SB") and (chosen_edge[0] == "BL" or chosen_edge[1] == "BL"):
            edge_distance = distance_SB_BL
        elif (chosen_edge[0] == "RM" or chosen_edge[1] == "RM") and (chosen_edge[0] == "SB" or chosen_edge[1] == "SB"):
            edge_distance = distance_RM_SB
        elif (chosen_edge[0] == "MV" or chosen_edge[1] == "MV") and (chosen_edge[0] == "RM" or chosen_edge[1] == "RM"):
            edge_distance = distance_MV_RM
        elif (chosen_edge[0] == "LA" or chosen_edge[1] == "LA") and (chosen_edge[0] == "MV" or chosen_edge[1] == "MV"):
            edge_distance = distance_LA_MV

        '''
        Because of the edges generated is from an undirected graph, the direction will always be the same. The only
        random choice made is just the choice of edge. The code statements below will randomly select the starting edge
        and the ending edge randomly to produce a random direction.
        '''
        start_vertex = random.choice(chosen_edge)
        chosen_edge.remove(start_vertex)
        end_vertex = chosen_edge[0]

        # Add the random edge
        (self.graph if selected_graph is None else selected_graph).add_weighted_edges_from([
            (start_vertex, end_vertex, edge_distance)
        ])

        return [start_vertex, end_vertex]