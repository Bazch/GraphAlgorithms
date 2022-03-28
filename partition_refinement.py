from graph_io import *


def color_refinement(G: Graph, C: Graph = None):
    partition = {}
    rho = {}
    for vertex in G.vertices:
        if vertex.label not in partition:
            partition[vertex.label] = [vertex]
        else:
            partition[vertex.label].append(vertex)

    for vertex in C.vertices:
        if vertex.label not in partition:
            partition[vertex.label] = [vertex]
        else:
            partition[vertex.label].append(vertex)

    for label in partition:
        isEqual = is_equal_vertices(G, partition[label])
        if not isEqual:
            return 0, partition
        if len(partition[label]) > 2:
            refine_partition(G, partition[label])

    for vertex in G.vertices:
        if hasattr(vertex, 'newlabel'):
            vertex.label = vertex.newlabel
            delattr(vertex, 'newlabel')
        if vertex.label not in rho:
            rho[vertex.label] = [vertex]
        else:
            rho[vertex.label].append(vertex)

    for vertex in C.vertices:
        if hasattr(vertex, 'newlabel'):
            vertex.label = vertex.newlabel
            delattr(vertex, 'newlabel')
        if vertex.label not in rho:
            rho[vertex.label] = [vertex]
        else:
            rho[vertex.label].append(vertex)

    if rho == partition:
        count = 0
        for label in rho:
            count += 1
        if count == len(G.vertices):
            return 1, partition
        return -1, partition

    return None, partition


def is_equal_vertices(G: Graph, vertices: list):
    count_g = 0
    count_c = 0
    for vertex in vertices:
        if vertex.graph == G:
            count_g += 1
        else:
            count_c += 1
    if count_g == count_c:
        return True
    else:
        return False


def refine_partition(G: Graph, vertices: list):
    neighbour_set = {}
    for i, vertex in enumerate(vertices):
        neighbours = []
        for neighbour in vertex.neighbours:
            neighbours.append(neighbour.label)
        neighbours.sort()
        neighbours_str = str(neighbours)
        if i == 0:
            neighbour_set[neighbours_str] = vertex
        elif neighbours_str not in neighbour_set:
            G.increase_highest_vertex()
            vertex.newlabel = G.highest_vertex
            neighbour_set[neighbours_str] = vertex
        else:
            same_vertex = neighbour_set.get(neighbours_str)
            if hasattr(same_vertex, 'newlabel'):
                vertex.newlabel = same_vertex.newlabel
            else:
                vertex.newlabel = same_vertex.label
