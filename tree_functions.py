from graph import *
from graph_io import *
from list_and_stack import *

def count_tree_isomorphisms(G: Graph, isDebug=False):

    while len(G.vertices) > 2:
        parent_dict = {}
        to_be_removed = []

        for vertex in G.vertices:
            if vertex.degree == 1:
                if not hasattr(vertex, 'code'):
                    vertex.code = f'({vertex.label if isDebug else ""})'
                    vertex.aut = 1
                parent = vertex.neighbours[0]
                parent.add_child(vertex)
                if parent in parent_dict:
                    parent_dict[parent].append(vertex)
                else:
                    parent_dict[parent] = [vertex]
                to_be_removed.append(vertex)

        for vertex in to_be_removed:
            G.remove_vertex(vertex)

        for parent in parent_dict:
            child_dict = {}
            codes = []
            codes2 = []

            if hasattr(parent, 'code'):
                codes.append(parent.code[1:-1])
            for vertex in parent_dict[parent]:
                codes.append(vertex.code)
            for vertex in parent.children:
                codes2.append(vertex.code)
            codes.sort()
            parent_encoding = ''
            for code in codes:
                parent_encoding = parent_encoding + code
            parent.code = f'({parent_encoding})'\





with open('graphs/trees36.grl') as f:
    graph_list = load_graph(f, read_list=True)

G = graph_list[0][0]

with open('graphs/results/before.dot', 'w') as f:
    write_dot(G, f)

count_tree_isomorphisms(G, False)

with open('graphs/results/after.dot', 'w') as f:
    write_dot(G, f)

for vertex in G.vertices:
    if hasattr(vertex, 'code'):
        print(vertex.code)
        print(vertex.children)