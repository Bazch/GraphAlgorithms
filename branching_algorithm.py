from graph import *
from graph_io import *
from partition_refinement import color_refinement
import sys
from profiler import profiler
from twin_detection import *


def count_isomorphisms(G: Graph, H: Graph, D:list, I: list, all_twins: list, count=False, useTwins=False):
    # Pre-processing
    for vertex in G.vertices:
        vertex.label = 0
    for vertex in H.vertices:
        vertex.label = 0
    if len(D) != 0:
        for i, vertex in enumerate(D):
            D[i].label = i+1
            I[i].label = i+1

    # Do color refinement
    result = None
    while result is None:
        result, partition = color_refinement(G,H)
    if result == 1 or result == 0:
        return result

    # Variables for the color/label to use (C) and which vertex to branch upon (vertex_x)
    C = -1
    vertex_x = None

    # See if a twin is in a color with 4 or more members
    # If there are twins in a color partition, set the color (C) and use one of the twins to branch upon (vertex_x)
    if useTwins:
        for twins in all_twins:
            for vertex in twins:
                if len(partition[vertex.label]) >= 4:
                    C = vertex.label
                    vertex_x = vertex
                    break
            # If we have found a twin, we don't need to keep looking for a vertex to branch upon
            if vertex_x is not None:
                break

    # If there are no twins, pick a color with the least amount of vertices (while still having at least 4)
    if vertex_x is None or C == -1:
        amount_of_vertices = sys.maxsize
        for label in partition:
            if amount_of_vertices > len(partition[label]) >= 4:
                C = label
                amount_of_vertices = len(partition[label])

    # Loop over all vertices in the partition and only collect the ones from graph H
    vertices_in_H = []
    for vertex in partition[C]:
        if vertex.graph == H:
            vertices_in_H.append(vertex)
        elif vertex_x is None:
            vertex_x = vertex

    # We create a copy from D and add our vertex_x to it for branching
    tempD = D[:]
    tempD.append(vertex_x)

    new_total = 0

    # Loop over all the collected vertices of graph H and call this function recursively
    # We use the vertices selected earlier from graph G and H in D and I respectively
    for vertex in vertices_in_H:
        # Make sure to copy the list and not actually change it, to make sure each iteration doesn't keep adding to I
        tempI = I[:]
        tempI.append(vertex)
        num = count_isomorphisms(G, H, tempD, tempI, all_twins, count=count, useTwins=useTwins)

        new_total = new_total + num
        if num > 0 and not count:
            return 1
        # If we only want to know if the graphs are isomorphic, we can stop once we found at least 1 automorphism
    return new_total

@profiler
def match_graphs_from_list(list_graphs):
    i = 0
    matching_graphs = []
    while i < len(list_graphs) - 1:
        j = i + 1
        if any(i in sl for sl in matching_graphs):
            i+=1
            continue
        else:
            while j < len(list_graphs):
                copy1, copy2 = list_graphs[i].deep_copy(), list_graphs[j].deep_copy()
                twins = count_twins(copy1)
                total = count_isomorphisms(copy1, copy2, [], [], twins, count=False, useTwins=False)
                if total > 0:
                    temp = [i,j, total]
                    matching_graphs.append(temp)
                j += 1
    for list in matching_graphs:
        print(str(list[0:2]) + " " + str(list[2]))

def count_leafs(G: Graph):
    leafs = 0
    for vertex in G.vertices:
        if vertex.degree == 1:
            leafs += 1
    return leafs

with open('graphs/cubes3.grl') as f:
    graph_list = load_graph(f, read_list=True)

match_graphs_from_list(graph_list[0])