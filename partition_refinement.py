from graph import *
from graph_io import *
from list_and_stack import *
from profiler import profiler


def match_graphs(list_graphs):
    discrete = []
    possibly_isomorph = []
    i = 0
    while i < len(list_graphs) - 1:
        j = i+1
        if any(i in sl for sl in discrete) or any(i in sl for sl in possibly_isomorph):
            i += 1
            continue
        else:
            iso = []
            dis = []
            while j < len(list_graphs):
                copy1, copy2 = list_graphs[i].deep_copy(), list_graphs[j].deep_copy()
                for vertex in copy1.vertices:
                    vertex.label = vertex.degree
                for vertex in copy2.vertices:
                    vertex.label = vertex.degree
                copy1.highest_vertex_number(), copy2.highest_vertex_number()
                result = None
                while result is None:
                    result, partition = color_refinement(copy1, copy2)
                if result == -1:
                    if i not in iso:
                        iso.append(i)
                    iso.append(j)
                if result == 1:
                    if i not in dis:
                        dis.append(i)
                    dis.append(j)
                j += 1
            if len(dis) > 0:
                discrete.append(dis)
            if len(iso) > 0:
                possibly_isomorph.append(iso)
            i += 1
    print("Possibly isomorph: ", possibly_isomorph)
    print("discrete: ", discrete)


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
        isEqual = is_equal_vertices(G, C, partition[label])
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

def is_equal_vertices(G: Graph, C: Graph, vertices: list):
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
            vertex.newlabel = G.highest_vertex
            G.increase_highest_vertex()
            neighbour_set[neighbours_str] = vertex
        else:
            same_vertex = neighbour_set.get(neighbours_str)
            if hasattr(same_vertex, 'newlabel'):
                vertex.newlabel = same_vertex.newlabel
            else:
                vertex.newlabel = same_vertex.label


with open('graphs/colorref_largeexample_4_1026.grl') as f:
    graph_list0 = load_graph(f, read_list=True)
with open('graphs/colorref_largeexample_6_960.grl') as f:
    graph_list1 = load_graph(f, read_list=True)
with open('graphs/colorref_smallexample_2_49.grl') as f:
    graph_list2 = load_graph(f, read_list=True)
with open('graphs/colorref_smallexample_4_16.grl') as f:
    graph_list3 = load_graph(f, read_list=True)
with open('graphs/colorref_smallexample_4_7.grl') as f:
    graph_list4 = load_graph(f, read_list=True)
with open('graphs/colorref_smallexample_6_15.grl') as f:
    graph_list5 = load_graph(f, read_list=True)
with open('graphs/cref9vert3comp_10_27.grl') as f:
    graph_list6 = load_graph(f, read_list=True)
with open('graphs/cref9vert_4_9.grl') as f:
    graph_list7 = load_graph(f, read_list=True)

all_graphs = [graph_list0,graph_list1,graph_list2,graph_list3,graph_list4,graph_list5,graph_list6,graph_list7]

@profiler
def do_all_graphs(list_graphs):
    print("\ncolorref_largeexample_4_1026")
    match_graphs(graph_list0[0])
    print("\ncolorref_largeexample_6_960")
    match_graphs(graph_list1[0])
    print("\ncolorref_smallexample_2_49")
    match_graphs(graph_list2[0])
    print("\ncolorref_smallexample_4_16")
    match_graphs(graph_list3[0])
    print("\ncolorref_smallexample_4_7")
    match_graphs(graph_list4[0])
    print("\ncolorref_smallexample_6_15")
    match_graphs(graph_list5[0])
    print("\ncref9vert_4_9")
    match_graphs(graph_list7[0])
    print("\ncref9vert3comp_10_27")
    match_graphs(graph_list6[0])

#do_all_graphs(all_graphs)
