from clean_slate_fast_color_partition import refine
from graph import *
from graph_io import *
from profiler import profile


def branch(mixed_graph: Graph, child_graph: Graph, D: list, I: list):

    tempD = D[:]
    tempI = I[:]

    for vertex in mixed_graph:
        vertex.colornum = 0

    i = 0
    if D:
        for vertex in D:
            D[i].colornum = i+1
            I[i].colornum = i+1
            i += 1

    mixed_graph.set_highest_vertex_colornum(i)
    result, partition = refine(mixed_graph, child_graph)

    if result == 1 or result == 0:
        return result

    best_color = None

    for color_key in partition:
        color1 = partition[color_key]
        offset = 4

        if len(color1.vertices) == 2:
            for vertex in color1.vertices:
                if vertex not in D and vertex not in I:
                    if vertex.original_graph == child_graph1:
                        tempD.append(vertex)
                    else:
                        tempI.append(vertex)
        elif len(color1.vertices) - offset == 0:
            best_color = color1
        elif len(color1.vertices) - offset > 0:
            best_color = color1

    vertex_x = None

    y_vertices = []
    for vertex in best_color.vertices:
        if vertex.original_graph == child_graph:
            vertex_x = vertex
        else:
            y_vertices.append(vertex)

    tempD.append(vertex_x)
    num = 0
    for vertex in y_vertices:
        tempI.append(vertex)
        num += branch(mixed_graph, child_graph, tempD, tempI)
        tempI.remove(vertex)

    return num

@profile
def run():
    with open('graphs/cubes5.grl') as f:
        graph_list = load_graph(f, read_list=True)

    G = graph_list[0][0]
    H = graph_list[0][1]

    I = G + H

    print(branch(I, G, [], []))


# run()

# with open('graphs/cubes5.grl') as f:
#     graph_list = load_graph(f, read_list=True)
#
# G = graph_list[0][0]
# H = graph_list[0][1]
#
# I = G+H
#
# print(branch(I, G, [], []))