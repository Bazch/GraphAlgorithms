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

    def __eq__(self, other):
        return self._id == other._id and len(self._vertices) == len(other._vertices)

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
            if neighbour.colornum not in color_dict:
                color_dict[neighbour.colornum] = {count: set()}
                color_dict[neighbour.colornum][count].add(neighbour)
            elif count not in color_dict[neighbour.colornum]:
                color_dict[neighbour.colornum][count] = set()
                color_dict[neighbour.colornum][count].add(neighbour)
            else:
                color_dict[neighbour.colornum][count].add(neighbour)
    return color_dict


def refine(graph: Graph):
    partition = collect_colors(graph)
    queue = doubly_linked_list()
    for color_id in partition:
        queue.append(partition[color_id])
        partition[color_id].set_in_queue()
    # queue.append(partition[0])
    # partition[0].set_in_queue()

    for current_color in queue:
        color_dict = refine_color(current_color)

        for color_key in color_dict:
            if not len(partition[color_key].vertices) > 1:
                continue
            number_of_neighbours_dict = color_dict[color_key]
            for count in number_of_neighbours_dict:
                if len(number_of_neighbours_dict[count]) < len(partition[color_key].vertices):
                    graph.increase_highest_colornum()
                    new_color = partition[color_key].split(graph.highest_colornum, number_of_neighbours_dict[count])
                    partition[new_color.id] = new_color

                    if len(new_color.vertices) < len(current_color.vertices) or current_color.is_in_queue:
                        queue.append(new_color)
                        new_color.set_in_queue()
                    else:
                        queue.append(current_color)
                        current_color.set_in_queue()

    if len(partition) == len(graph.vertices):
        return 1, partition

    return -1, partition


def count_isomorphisms(G: Graph, H: Graph, D: list, I: list, all_twins: list, count=False, useTwins=False):
    # Pre-processing
    tempD = D[:]
    tempI = I[:]

    for vertex in G.vertices:
        vertex.colornum = 0
    for vertex in H.vertices:
        vertex.colornum = 0

    i = 0
    if D:
        for vertex in D:
            D[i].colornum = i + 1
            I[i].colornum = i + 1
            i += 1

    G.set_highest_vertex_colornum(i)
    H.set_highest_vertex_colornum(i)

    result1, partition1 = refine(G)
    result2, partition2 = refine(H)

    result = -1
    if partition1 != partition2:
        result = 0
    elif result1 == 1:
        result = 1

    if result == 1 or result == 0:
        return result

    vertex_x = None

    best_color1 = None
    best_color2 = None

    for color_key in partition1:
        color1 = partition1[color_key]
        offset = 2

        if len(color1.vertices) == 1:
            tempD.append(color1.vertices.head.data)
            tempI.append(partition2[color_key].vertices.head.data)
        elif len(color1.vertices) - offset == 0:
            best_color1 = color1
            best_color2 = partition2[color_key]
            break
        elif len(color1.vertices) - offset > 0:
            best_color1 = color1
            best_color2 = partition2[color_key]

    vertex_x = best_color1.vertices.head.data
    tempD.append(vertex_x)

    num = 0

    for vertex_y in best_color2.vertices:
        tempI.append(vertex_y)
        num += count_isomorphisms(G, H, tempD, tempI, [], count=count, useTwins=useTwins)
        tempI.remove(vertex_y)

        if num > 0 and not count:
            return num

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
                    new_total = compare_graphs(graphs[0], graphs[2], slow_index, fast_index,
                                               use_twins, count)
                    # new_total = compare_graphs(graphs[slow_index], graphs[fast_index], slow_index, fast_index,
                    #                            use_twins, count)
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
        "cubes": [3],
        # "modules": ["C", "D"],
        # "products": [72, 216],
        # "torus": [24, 72, 144],
        # "torus": [24, 72, 144]
        # "trees": [11, 36, 90],
        # "wheeljoin": [14, 19, 25, 33],
        # "wheelstar": [12, 15, 16]
    }
    extension = ".grl"

    for sample_name in sample_names:
        for identifier in sample_names[sample_name]:
            run(f'{base_path}/{sample_name}{identifier}{extension}', use_twins, count)


# run_count_sample(use_twins=True, count=True)

with open('graphs/results/example.gr') as f:
    g = load_graph(f)
    with open('before.dot', 'w') as b:
        write_dot(g, b)
    for vertex in g:
        vertex.colornum = 0
    refine(g)
    with open('after.dot', 'w') as a:
        write_dot(g, a)
