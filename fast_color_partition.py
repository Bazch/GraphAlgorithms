from graph import *
from graph_io import load_graph, write_dot
from list_and_stack import doubly_linked_list


class ColorClass:

    def __init__(self, label, vertices=doubly_linked_list()):
        self._v = vertices
        self._label = label
        self._in_queue = False

    def __len__(self) -> int:
        """
        :return: The number of vertices of the graph
        """
        return len(self._v)

    def __str__(self) -> str:
        return f'ColorClass: {self._label} V=[' + ", ".join(map(str, self._v)) + ']'

    @property
    def vertices(self) -> doubly_linked_list:
        return self._v

    @property
    def label(self) -> int:
        return self._label

    @property
    def in_queue(self) -> bool:
        return self._in_queue

    def is_in_queue(self, b: bool):
        self._in_queue = b

    def add_vertex(self, v: Vertex):
        self._v.append(v)

    def remove_vertex(self, v: Vertex):
        self._v.remove(v)


def refine(G: Graph):
    color_classes = {}
    partition = doubly_linked_list()
    for vertex in G:
        if vertex.label not in color_classes:
            color_classes[vertex.label] = doubly_linked_list()
        color_classes[vertex.label].append(vertex)
    for label in color_classes:
        c = ColorClass(label, color_classes[label])
        partition.append(c)

    color_queue = doubly_linked_list()
    color_queue.append(partition.head.data)
    for C in color_queue:
        neighbours = set()
        current_color = C.label
        color_dict = {}
        # iterate all vertices in C (q ϵ C)
        for vertex in C.vertices:
            # iterate all neighbours of each vertex (q' ϵ Nx-(q)
            for n in vertex.neighbours:
                neighbours.add(n)
        for n in neighbours:
            count = 0
            # iterate its neighbours in turn to see how many neighbours they have in the current color class
            for neighbour in n.neighbours:
                if neighbour.label == current_color:
                    count += 1
            if n.label not in color_dict:
                color_dict[n.label] = {count: doubly_linked_list()}
                color_dict[n.label][count].append(n)
            elif count not in color_dict[n.label]:
                color_dict[n.label][count] = doubly_linked_list()
                color_dict[n.label][count].append(n)
            else:
                color_dict[n.label][count].append(n)

        discreet_partitions = 0
        for color in partition:
            if len(color) % 2 != 0:
                return 0, partition

            if len(color) == 2:
                discreet_partitions += 1

            if color.label in color_dict and len(color) > 2:
                for number_neighbours in color_dict[color.label]:
                    if len(color_dict[color.label][number_neighbours]) < len(color):
                        G.increase_highest_vertex()
                        new_color = ColorClass(G.highest_vertex, color_dict[color.label][number_neighbours])
                        partition.append(new_color)
                        for vertex in new_color.vertices:
                            vertex.new_label = new_color.label
                            color.vertices.remove(vertex)
                        if len(new_color) < len(color) or color.in_queue:
                            color_queue.append(new_color)
                        else:
                            color_queue.append(color)
        if discreet_partitions == len(partition):
            return 1, partition

        for vertex in G.vertices:
            if hasattr(vertex, 'new_label'):
                vertex.label = vertex.new_label
                delattr(vertex, 'new_label')
    return -1, partition

with open('graphs/colorref_smallexample_4_16.grl') as f:
    graph_list = load_graph(f, read_list=True)

G = graph_list[0][0]
H = graph_list[0][1]
I = G+H
DLL1 = doubly_linked_list()

for vertex in I:
    vertex.label = 0
    DLL1.append(vertex)

ColorClass1 = ColorClass(0, DLL1)
partition = doubly_linked_list()
partition.append(ColorClass1)
I.highest_vertex_number()

with open('graphs/results/example1.dot', 'w') as f:
    write_dot(I, f)

print(refine(I))

with open('graphs/results/example2.dot', 'w') as f:
    write_dot(I, f)

