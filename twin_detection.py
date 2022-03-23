from graph import *
from graph_io import *


def count_twins(G: Graph):
    all_twins = []
    for vertex in G.vertices:
        twins = []
        for other_vertex in G.vertices:
            if vertex == other_vertex:
                continue
            vertex_neighbourhood = vertex.neighbours[:]
            other_vertex_neighbourhood = other_vertex.neighbours[:]
            if other_vertex in vertex_neighbourhood:
                vertex_neighbourhood.remove(other_vertex)
            if vertex in other_vertex_neighbourhood:
                other_vertex_neighbourhood.remove(vertex)
            areEqual = list_similar_content(vertex_neighbourhood, other_vertex_neighbourhood)
            if areEqual:
                if any(vertex in sl for sl in all_twins):
                    break
                elif vertex in twins:
                    twins.append(other_vertex)
                else:
                    twins.append(vertex)
                    twins.append(other_vertex)
        if len(twins) > 0:
            all_twins.append(twins)
    return all_twins

def list_similar_content(list1, list2):
    for x in set(list1 + list2):
        if list1.count(x) != list2.count(x):
            return False
    return True

"""
G = Graph(True, n=5)
G.add_edge(Edge(G.vertices[0], G.vertices[1]))
G.add_edge(Edge(G.vertices[1], G.vertices[2]))
G.add_edge(Edge(G.vertices[0], G.vertices[3]))
G.add_edge(Edge(G.vertices[3], G.vertices[2]))
G.add_edge(Edge(G.vertices[0], G.vertices[4]))
G.add_edge(Edge(G.vertices[4], G.vertices[2]))
G.add_edge(Edge(G.vertices[4], G.vertices[3]))

with open('graphs/results/example.gr', 'w') as f:
    save_graph(G,f)

with open('graphs/results/example.dot', 'w') as f:
    write_dot(G,f)

with open('graphs/wheeljoin14.grl') as f:
    graph_list = load_graph(f, read_list=True)

H = graph_list[0][0]

    
test = count_twins(H)
print(test)
"""