from graph import *
from graph_io import *
from list_and_stack import *
import random as rd


def connected_BFS(G: Graph):
    queue = doubly_linked_list()
    start = G.vertices[0]
    queue.append(start)
    visited = [start]

    for i, node in enumerate(queue):
        vertex = node.data
        for neighbour in vertex.neighbours:
            if neighbour not in visited:
                queue.append(neighbour)
                visited.append(neighbour)
        # vertex.label = i
    connected = i == len(G.vertices)-1
    return connected


def connected_DFS(G: Graph):
    s = stack()
    start = G.vertices[0]
    s.push(start)
    visited = []
    i = 0
    while not s.isEmpty():
        vertex = s.pop()
        if vertex not in visited:
            visited.append(vertex)
            # vertex.label = vertex.degree
            for neighbour in vertex.neighbours:
                s.push(neighbour)
            i += 1
    connected = i == len(G.vertices)
    return G, connected
