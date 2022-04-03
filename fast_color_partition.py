from graph import *
from graph_io import load_graph, write_dot
from list_and_stack import doubly_linked_list


class ColorClass:

    def __init__(self, label, vertices: doubly_linked_list()):
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
        self._v.push(v)

    def remove_vertex(self, v: Vertex):
        self._v.remove(v)

    def split(self, new_label: int, vertices_to_be_split: set):
        new_color = ColorClass(new_label, doubly_linked_list())
        for node in self._v:
            if node.data in vertices_to_be_split:
                node.data.label = new_color.label
                new_color.vertices.push(node.data)
                self._v.remove_node(node)

        return new_color

def refine(G: Graph):
    color_classes = {}
    partition = doubly_linked_list()

    for vertex in G:
        if vertex.label not in color_classes:
            color_classes[vertex.label] = doubly_linked_list()
        color_classes[vertex.label].push(vertex)

    for label in color_classes:
        c = ColorClass(label, color_classes[label])
        partition.push(c)

    color_queue = doubly_linked_list()
    color_queue.append(partition.head.data)
    partition.head.data.is_in_queue(True)

    for color_queue_node in color_queue:
        C = color_queue_node.data
        neighbours = set()
        current_color = C.label
        color_dict = {}

        # iterate all vertices in C (q ϵ C)
        for color_vertex_node in C.vertices:
            # iterate all neighbours of each vertex (q' ϵ Nx-(q)
            for n in color_vertex_node.data.neighbours:
                neighbours.add(n)

        for n in neighbours:
            count = 0
            # iterate its neighbours in turn to see how many neighbours they have in the current color class
            for neighbour in n.neighbours:
                if neighbour.label == current_color:
                    count += 1
            if n.label not in color_dict:
                color_dict[n.label] = {count: set()}
                color_dict[n.label][count].add(n)
            elif count not in color_dict[n.label]:
                color_dict[n.label][count] = set()
                color_dict[n.label][count].add(n)
            else:
                color_dict[n.label][count].add(n)

        for color_class_node in partition:

            if color_class_node.data.label in color_dict and len(color_class_node.data) > 2:
                for number_neighbours in color_dict[color_class_node.data.label]:

                    if len(color_dict[color_class_node.data.label][number_neighbours]) < len(color_class_node.data):
                        G.increase_highest_vertex()
                        new_color = color_class_node.data.split(G.highest_vertex, color_dict[color_class_node.data.label][number_neighbours])

                        partition.push(new_color)

                        if len(new_color) < len(color_class_node.data) or color_class_node.data.in_queue:
                            color_queue.append(new_color)
                            new_color.is_in_queue(True)

                        else:
                            color_queue.append(color_class_node.data)
                            color_class_node.data.is_in_queue(True)

    discreet_partitions = 0
    for color in partition:

        if len(color.data) % 2 != 0:
            return 0, partition

        if len(color.data) == 2:
            discreet_partitions += 1

    if discreet_partitions == len(partition):
        return 1, partition

    return -1, partition

# with open('graphs/colorref_smallexample_4_16.grl') as f:
#     graph_list = load_graph(f, read_list=True)
#
# G = graph_list[0][0]
# H = graph_list[0][1]
# I = G+H
# DLL1 = doubly_linked_list()
#
# for vertex in I:
#     vertex.label = 0
#
# I.highest_vertex_number()
#
# with open('graphs/results/example1.dot', 'w') as f:
#     write_dot(I, f)
#
# print(refine(I))
#
# with open('graphs/results/example2.dot', 'w') as f:
#     write_dot(I, f)

