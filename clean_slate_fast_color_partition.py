from color_class import ColorClass
from graph import *
from graph_io import *
from list_and_stack import doubly_linked_list


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


def refine(graph: Graph, other_graph: Graph):
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
    is_equal = check_if_equal_partition(partition, other_graph)
    if not is_equal:
        return 0, partition

    if len(partition) == len(graph.vertices) / 2:
        return 1, partition

    return -1, partition


def check_if_equal_partition(partition: dict, G: Graph):
    for color_key in partition:
        count_g = 0
        count_h = 0
        for vertex in partition[color_key].vertices:
            if vertex.original_graph == G:
                count_g += 1
            else:
                count_h += 1
        if count_g != count_h:
            return False
    return True

# with open('graphs/results/example2.gr') as f:
#     G = load_graph(f)
#
#
#
# for i, vertex in enumerate(G):
#     vertex.colornum = 0
#
#
#
# with open('graphs/results/example2_before.dot', 'w') as f:
#     write_dot(G, f)
#
# refine(G)
# with open('graphs/results/example2_after1.dot', 'w') as f:
#     write_dot(G, f)



# with open('graphs/cubes6.grl') as f:
#     graph_list = load_graph(f, read_list=True)
#
# G = graph_list[0][0]
# H = graph_list[0][1]
#
# I = G + H
#
# for vertex in I:
#     vertex.colornum = 0
#
# print(refine(I, G))