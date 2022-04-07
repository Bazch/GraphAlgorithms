from graph import *
from list_and_stack import doubly_linked_list


class ColorClass:
    _id = None
    _is_in_queue = False
    _vertices = doubly_linked_list()

    def __init__(self, id: int, vertices: doubly_linked_list):
        self._id = id
        self._vertices = vertices

    def __str__(self) -> str:
        return f'ColorClass: {self._id} V=[' + ", ".join(map(str, self._vertices)) + ']'

    def __eq__(self, other):
        return len(self._vertices) == len(other._vertices)

    @property
    def vertices(self) -> doubly_linked_list:
        return self._vertices

    @property
    def id(self) -> int:
        return self._id

    @property
    def is_in_queue(self):
        return self._is_in_queue

    def set_in_queue(self):
        self._is_in_queue = True

    def add_vertex(self, v: Vertex):
        self._vertices.push(v)

    def remove_vertex(self, v: Vertex):
        self._vertices.remove(v)

    def split(self, new_id: int, vertices_to_be_split: set):
        new_color = ColorClass(new_id, doubly_linked_list())
        self._vertices.set_iter_nodes(True)
        for node in self._vertices:
            vertex = node.data
            if vertex in vertices_to_be_split:
                vertex.colornum = new_color.id
                self._vertices.remove_node(node)
                new_color.add_vertex(vertex)
        self._vertices.set_iter_nodes(False)

        return new_color
