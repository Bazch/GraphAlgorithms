from graph import Graph
from list_and_stack import doubly_linked_list


class color_class:

    def __init__(self, label, vertices=doubly_linked_list()):
        self._vertices = vertices
        self._size = len(vertices)
        self._label = label
        self._in_queue = False

    @property
    def vertices(self) -> doubly_linked_list:
        return self._vertices

    @property
    def size(self) -> int:
        return self._size

    @property
    def label(self) -> int:
        return self._label

    @property
    def in_queue(self) -> bool:
        return self._in_queue

    def is_in_queue(self, b: bool):
        self._in_queue = b


def refine(C: color_class, x: int):

    color_queue = doubly_linked_list()
    all_states_in_Ci = doubly_linked_list()

    current_color = 0
    L = doubly_linked_list()

    # iterate all vertices in C (q ϵ C)

    for vertex in C.vertices:
        A = doubly_linked_list()
        # iterate all neighbours of each vertex (q' ϵ Nx-(q)
        for n in vertex.neighbours:
            count = 0
            # iterate its neighbours in turn to see how many neighbours they have in the current color class
            for neighbour in n.neighbours:
                if neighbour.label == current_color:
                    count += 1
            if count == x:
                A.push(neighbour)
    if len(A) > 0:
        L.push(A)

    for list in L:
        if len(list) < len(all_states_in_Ci):
            # split to new color l
            # add smallest to color_queue
            pass

    pass
