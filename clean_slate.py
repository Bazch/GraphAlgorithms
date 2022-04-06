from list_and_stack import doubly_linked_list
from tree_functions import *
from twin_detection import *


class ColorClass:
    _id = None
    _is_in_queue = False
    _vertices = doubly_linked_list()

    def __init__(self, id: int, vertices: doubly_linked_list):
        self._id = id
        self._vertices = vertices

    def __str__(self) -> str:
        return f'ColorClass: {self._id} V=[' + ", ".join(map(str, self._vertices)) + ']'

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


def collect_colors(graph: Graph):
    color_classes = {}
    for vertex in graph:
        if vertex.colornum not in color_classes:
            color_classes[vertex.colornum] = ColorClass(vertex.colornum, doubly_linked_list())
            color_classes[vertex.colornum].add_vertex(vertex)
        else:
            color_classes[vertex.colornum].add_vertex(vertex)
    return color_classes


def refine_color(color: ColorClass):
    color_dict = {}
    for vertex in color.vertices:
        for neighbour in vertex.neighbours:
            count = 0
            for neighbouring_vertex in neighbour.neighbours:
                if neighbouring_vertex.colornum == vertex.colornum:
                    count += 1
            if vertex.colornum not in color_dict:
                color_dict[vertex.colornum] = {count: set()}
                color_dict[vertex.colornum][count].add(neighbour)
            elif count not in color_dict[vertex.colornum]:
                color_dict[vertex.colornum][count] = set()
                color_dict[vertex.colornum][count].add(neighbour)
            else:
                color_dict[vertex.colornum][count].add(neighbour)
    return color_dict


def refine(graph: Graph):
    partition = collect_colors(graph)
    queue = doubly_linked_list()
    queue.append(partition[0])
    partition[0].set_in_queue()

    for current_color in queue:
        color_dict = refine_color(current_color)

        for color_key in color_dict:
            number_of_neighbours_dict = color_dict[color_key]
            for count in number_of_neighbours_dict:
                if 2 < len(color_dict[color_key][count]) < len(current_color.vertices):
                    graph.increase_highest_vertex()
                    new_color = current_color.split(graph.highest_vertex, color_dict[color_key][count])
                    partition[new_color.id] = new_color

                    if len(new_color.vertices) < len(current_color.vertices) or current_color.is_in_queue:
                        queue.append(new_color)
                        new_color.set_in_queue()
                    else:
                        queue.append(current_color)
                        current_color.set_in_queue()

    return 1, partition


def count_isomorphisms(G: Graph, H: Graph, D:list, I: list, all_twins: list, count=False, useTwins=False):
    # Pre-processing
    tempD = D[:]
    tempI = I[:]

    for vertex in G.vertices:
        vertex.colornum = 0
    for vertex in H.vertices:
        vertex.colornum = 0

    if len(D) >= 1 and D[0] is not None:
        for i, vertex in enumerate(D):
            D[i].colornum = i+1
            I[i].colornum = i+1

    # result, partition_g, partition_h = refine(G, H)
    result = refine(G)

    if result == 1 or result == 0:
        return result

    vertex_x = None

    # See if a twin is in a color with 4 or more members
    # If there are twins in a color partition, set the color (C) and use one of the twins to branch upon (vertex_x)
    if useTwins:
        for twins in all_twins:
            for vertex in twins:
                for color in partition_g:
                    if len(color) >= 2:
                        C = color
                        vertex_x = vertex
                        break
                # If we have found a twin, we don't need to keep looking for a vertex to branch upon
                if vertex_x is not None:
                    break

    num = 0

    # Loop over all the collected vertices of graph H and call this function recursively
    # We use the vertices selected earlier from graph G and H in D and I respectively
    for vertex in c_h.vertices:
        # Make sure to copy the list and not actually change it, to make sure each iteration doesn't keep adding to I

        if len(tempI) < len(tempD):
            tempI.append(vertex.data)
        else:
            tempI[len(tempD) - 1] = vertex.data
        num += count_isomorphisms(G, H, tempD, tempI, all_twins, count=count, useTwins=useTwins)
        if num > 0 and not count:
            return num
        # If we only want to know if the graphs are isomorphic, we can stop once we found at least 1 automorphism

    return num


def compare_trees(G: Graph, H: Graph):
    code_c, aut_c = count_tree_isomorphisms(G)
    code_h, aut_h = count_tree_isomorphisms(H)
    if code_c != code_h:
        return 0
    return aut_c


def compare_graphs(G: Graph, H: Graph, g_label, h_label, use_twins, count):
    copy1, copy2 = G.deep_copy(), H.deep_copy()
    is_tree1, is_tree2 = is_graph_tree(copy1), is_graph_tree(copy2)
    if is_tree1:
        if not is_tree2:
            return 0
        total = compare_trees(copy1, copy2)
        return total

    twins = count_twins(copy1)

    # attempt at the disjoint union approach
    # I = copy1+copy2
    # total = count_isomorphisms(I, copy2, [], [], twins, useTwins=use_twins, count=count)

    total = count_isomorphisms(copy1, copy2, [], [], twins, useTwins=use_twins, count=count)
    # total = count_isomorphisms(G, H, [], [], twins, useTwins=use_twins, count=count)

    return total


def run(path, use_twins: bool, count: bool):
    with open(path) as f:
        comparison_graphs = load_graph(f, read_list=True)

    matching_graphs = []

    print(path)
    if count:
        print('Sets of isomorphic graphs and the number of automorphisms:')
    else:
        print('Sets of isomorphic graphs:')

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
                    new_total = compare_graphs(graphs[slow_index], graphs[fast_index], slow_index, fast_index, use_twins, count)
                    if new_total != 0:
                        temp.append(fast_index)
                        total = new_total
                fast_index += 1

            if len(temp) > 0:
                temp.insert(0, slow_index)
                matching_graphs.append(temp)
                if count:
                    print(f'{temp} {total}')
                else:
                    print(f'{temp}')

            slow_index += 1
            fast_index = 0
    print('')


@profile
def run_count_sample(use_twins: bool, count: bool):
    base_path = "graphs"
    sample_names = {
        # "bigtrees": [1, 2, 3],
        # "cographs": [1],
        # "cubes": [3, 4, 5, 6, 7, 8, 9],
        # "modules": ["C", "D"],
        # "products": [72, 216],
        # "torus": [24, 72, 144],
        # "torus": [24, 72, 144]
        # "trees": [11, 36, 90],
        # "wheeljoin": [14, 19, 25, 33],
        "wheeljoin": [14],
        # "wheelstar": [12, 15, 16]
    }
    extension = ".grl"

    for sample_name in sample_names:
        for identifier in sample_names[sample_name]:
            run(f'{base_path}/{sample_name}{identifier}{extension}', use_twins, count)


run_count_sample(use_twins=True, count=True)
