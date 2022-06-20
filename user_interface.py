import graph_functions
import os

def menu():
    print(
        """
        _________________________________________
                       FUNCTIONS
        _________________________________________
        Choose to perform:
        1: Check whether the graph is strongly connected
        2: Check whether the graph has any cycle
        3: Check the shortest path between 2 vertices
        4: Check the Minimum Spanning Tree (MST)
        """
        )


def user_input():
    choice = int(input("Choice: "))
    try:
        while choice < 1 or choice > 8:
            print("This is invalid choice. Try again!")
            choice = int(input("Choice: "))
    except ValueError:
        print("This is invalid choice. Try again!")
    return choice


def function_interface(choice, graph):
    if choice == 1:
        os.system('cls')
        print("==============================================================")
        print("| Function 1:  Check whether the graph is strongly connected |")
        print("==============================================================")
        graph.function_one()
    
    elif choice == 2:
        os.system('cls')
        print("======================================================")
        print("| Function 2:  Check whether the graph has any cycle |")
        print("======================================================")
        graph.function_two()
    
    elif choice == 3:
        os.system('cls')
        print("===========================================================")
        print("| Function 3:  Check the shortest path between 2 vertices |")
        print("===========================================================")

        print("\nWhich path would you like to find?")
        print("\nEnter any one of the city abbreviation as follow" +
              "\n[LA / BL / SB / RM / MV]")
        start_vertex = input("From: ")
        end_vertex = input("To: ")
        graph.function_three(start_vertex, end_vertex)
    
    elif choice == 4:
        os.system('cls')
        print("===========================================================")
        print("| Function 4:  Check the Minimum Spanning Tree (MST)      |")
        print("===========================================================")

        print("Available Edges: ", [i for i in graph.removable_edges()], "\n")
        select_edge = []
        start_vertex = input("\nFrom: ")
        end_vertex = input("To: ")
        if (start_vertex, end_vertex) not in select_edge and (start_vertex, end_vertex) in graph.removable_edges():
            select_edge.append((start_vertex, end_vertex))
        else:
            print("Invalid input, this could be because the selected edge is already chosen, "
                  "or not in the graph.")

        while True:
            print("Available Edges: ", [i for i in graph.removable_edges() if i not in select_edge], "\n")
            more_edges = str(input("\nSelect more available edge to generate MST? [y/n]")).lower()
            if more_edges == 'n':
                break
            elif more_edges == 'y':
                start_vertex = input("\nFrom: ")
                end_vertex = input("To: ")
                if (start_vertex, end_vertex) not in select_edge and (start_vertex, end_vertex) in graph.removable_edges():
                    select_edge.append((start_vertex, end_vertex))
                else:
                    print("Invalid input, this could be because the selected edge is already chosen, "
                          "or not in the graph.")
            else:
                print("Invalid Input!")

        if len(select_edge) > 0:
            mst = graph.function_four(select_edge)
            graph.print_graph(selected_graph=mst, curve=False, title="Minimum Spanning Tree")
        else:
            print("No edges was selected.")
        
