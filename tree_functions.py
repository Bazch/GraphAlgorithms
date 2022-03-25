import math

from profiler import profile
from graph import *
from graph_io import *
from search_algorithms import connected_DFS


def is_graph_tree(G: Graph):
    is_connected = connected_DFS(G)
    if not is_connected:
        return False
    v = len(G.vertices)
    e = len(G.edges)
    if (v-e) == 1:
        return True
    return False


#@profile
def count_tree_isomorphisms(G: Graph, isDebug=False):

    # Loop until we find the center node(s), which are at most 2
    while len(G.vertices) > 2:

        # Initiate a set for all parents and a list for the nodes that need to be removed
        parents = set()
        to_be_removed = []

        # Loop over all vertices, and pick the leafs (degree 1)
        for vertex in G.vertices:
            if vertex.degree == 1:

                # If a vertex has not yet received a code, it's a 'true' leaf and gets a basic encoding of '()'
                # Additionally, it gets an automorphism value of 1, since the leaf itself has 1 permutation
                if not hasattr(vertex, 'code'):
                    vertex.code = f'({vertex.label if isDebug else ""})'
                    vertex.aut = 1

                # Assign the parent for easy readability and add its current child to its list of children
                # Since vertex has a degree of 1, its first neighbour must be it's 'parent'
                parent = vertex.neighbours[0]
                parent.add_child(vertex)

                # We mark all visited vertices to be deleted and aggregate their parents
                parents.add(parent)
                to_be_removed.append(vertex)

        # Once all vertices have been visited this iteration, we can safely remove them
        # Removing them gives us a new set of 'leafs' for the next iteration
        for vertex in to_be_removed:
            G.remove_vertex(vertex)

        # Loop over all parents and initiate some values
            # A list of codes to aggregate the codes of the parent's children
            # A dictionary to keep track of how many unique codes this parent has
            # 'aut' is set to 1 for now, since we don't know the parent's value yet
        for parent in parents:
            codes = []
            child_dict = {}
            aut = 1

            # We loop over all children of a 'parent' node and map them according to their codes
            # Additionally we save all codes in a list
            for vertex in parent.children:
                codes.append(vertex.code)
                if vertex.code in child_dict:
                    child_dict[vertex.code].append(vertex)
                else:
                    child_dict[vertex.code] = [vertex]

            # Now we calculate the value of the parent node according to the following formula
                # Π_children.aut * Π_(number_similar_children!)
                # for a parent node with 1 pair of identical children (child1&child2) it would be:
                    # child1.aut * child2.aut * child3.aut * child4.aut * 2! * 1! * 1!
            for code in child_dict:
                for vertex in child_dict[code]:
                    aut = aut * vertex.aut
                aut = aut * math.factorial(len(child_dict[code]))
            parent.aut = aut

            # We sort the list with codes (! important) and initialize parent encoding
            codes.sort()
            parent_encoding = ''

            # We append all children codes and wrap them in brackets to obtain a unique code for this subtree
            for code in codes:
                parent_encoding = parent_encoding + code
            parent.code = f'({parent_encoding})'

    # If there are exactly 2 vertices left, we have a center with 2 nodes
    # We create a third node, and make it the root of the tree and enter this function again
        # This will correctly calculate the result
    if len(G.vertices) == 2:
        x = Vertex(G)
        G.remove_edge(G.edges[0])
        G.add_edge(Edge(x, G.vertices[0]))
        G.add_edge(Edge(x, G.vertices[1]))

        count_tree_isomorphisms(G)

    # We return the final code of this tree, and the amount of automorphisms.
        # If the code matches that of another tree, they are isomorphic
    return G.vertices[0].code, G.vertices[0].aut
