from profiler import *
from graph import *
from graph_io import *
from partition_refinement import color_refinement
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
    G.highest_vertex_number(), H.highest_vertex_number()
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

    num = 0

    # Loop over all the collected vertices of graph H and call this function recursively
    # We use the vertices selected earlier from graph G and H in D and I respectively
    for vertex in vertices_in_H:
        # Make sure to copy the list and not actually change it, to make sure each iteration doesn't keep adding to I
        tempI = I[:]
        tempI.append(vertex)
        num += count_isomorphisms(G, H, tempD, tempI, all_twins, count=count, useTwins=useTwins)

        if num > 0 and not count:
            return num
        # If we only want to know if the graphs are isomorphic, we can stop once we found at least 1 automorphism
    return num


def compare_graphs(G: Graph, H: Graph, g_label, h_label):
    copy1, copy2 = G.deep_copy(), H.deep_copy()
    twins = count_twins(copy1)
    total = count_isomorphisms(copy1, copy2, [], [], twins, useTwins=True, count=True)

    return total


def run(path):
    with open(path) as f:
        comparison_graphs = load_graph(f, read_list=True)

    matching_graphs = []
    
    print(path)
    print('Sets of possibly isomorphic graphs:')

    slow_index = 0
    fast_index = 0

    for graphs in comparison_graphs:
        number_of_graphs = len(graphs)

        while slow_index < number_of_graphs:
            if any(slow_index in sl for sl in matching_graphs):
                slow_index += 1
                continue

            temp = []
            total = 0

            while fast_index < number_of_graphs:
                if slow_index < fast_index:
                    new_total = compare_graphs(graphs[slow_index], graphs[fast_index], slow_index, fast_index)
                    if new_total != 0:
                        temp.append(fast_index)
                        total = new_total
                fast_index += 1

            if len(temp) > 0:
                temp.insert(0, slow_index)
                matching_graphs.append(temp)
                print(f'{temp} {total}')

            slow_index += 1
            fast_index = 0
    print('')


@profile
def run_count_sample():
    base_path = "graphs"
    sample_names = {
        # "bigtrees": [1, 2, 3],
        # "cographs": [1],
        # "cubes": [3, 4, 5, 6, 7, 8, 9],
        # "modules": ["C", "D"],
        # "products": [72, 216],
        "products": [72],
        "torus": [24],
        # "torus": [24, 72, 144],
        # "trees": [11, 36, 90],
        # "wheeljoin": [14, 19, 25, 33],
        # "wheelstar": [12, 15, 16]
    }
    extension = ".grl"

    for sample_name in sample_names:
        for identifier in sample_names[sample_name]:
            run(f'{base_path}/{sample_name}{identifier}{extension}')


run_count_sample()
