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
    
    # Display list of edges in the graph to ease user to select
    def available_edges(self):
        return list(nx.non_edges(self.graph))

    # Display list of removable edges to ease user to select which to remove
    def removable_edges(self):
        return list(nx.edges(self.graph))
    
    # Restriction for edge selection
    def edge_input_validation(self, start_vertex, end_vertex):
        if (start_vertex, end_vertex) in self.graph.edges:
            print("Edge already exists! Try another one.")
            return False
        elif (start_vertex, end_vertex) not in self.available_edges():
            print("Invalid Edge! Try another one.")
            return False
        else:
            return True
        
    # Check strong connectivity
    def function_one(self):
        # List of random added edges
        added_edges = []
        
        # Determine if the graph is strongly connected by using the networkx built-in function is_strongly_connected
        # This function returns True is it is a strongly connected graph
        print("\nStrongly Connected Graph: " + str(nx.is_strongly_connected(self.graph)))
        input("\nPress any key to continue...")
        
        # Generate random edge until a strongly connected graph is found
        while not nx.is_strongly_connected(self.graph):
            added_edges.append(self.add_random_edge())

        # Prompt user to press any key to proceed to viewing the results
        input("\nPress any key to view the graph.")
        os.system('cls') # clear the screen
        
        # Print the graph after a strongly connected graph is found
        print("\nStrongly Connected Graph: " + str(nx.is_strongly_connected(self.graph)))
        
        # Only display the added edges if any edges is added 
        if len(added_edges) != 0:   
            print("\nNumber of Added Edges: ", len(added_edges))
            print("Randomly Added edges: ", [i for i in added_edges])
            
        self.print_graph(title="Strongly Connected Graph")
        self.print_adjacency_list()

    # Check if got cycle
    def function_two(self):
        while not self.has_cycle():
            print("Graph does not has a cycle, adding random edges.")
            self.add_random_edge()
        cycle_path = sorted(nx.simple_cycles(self.graph))[0]
        print("The cycle within the graph is from: " + str(cycle_path))

        subgraph = self.graph.subgraph(cycle_path)
        self.print_graph(selected_graph=subgraph, title="The graph cycle")
        self.print_adjacency_list()