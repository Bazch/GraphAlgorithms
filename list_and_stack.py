import gc
from graph import *

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class doubly_linked_list:

    def __len__(self):
        return self.size

    def __init__(self):
        self.head = None
        self.size = 0

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

    def __reversed__(self):
        current = self.head
        while current.next is not None:
            current = current.next
        while current is not None:
            yield current
            current = current.prev

    def __repr__(self):
        string = "["
        if self.head is not None:
            current = self.head
            string += str(current.data)
            current = current.next
            while (current is not None):
                string += f', {current.data}'
                current = current.next
        string += ']'
        return string

    def push(self, new_val):
        new_node = Node(new_val)
        new_node.next = self.head
        if self.head is not None:
            self.head.prev = new_node
        self.head = new_node
        self.size += 1

    def append(self, new_val):
        new_node = Node(new_val)
        new_node.next = None
        if self.head is None:
            new_node.prev = None
            self.head = new_node
            self.size += 1
            return
        last = self.head
        while last.next is not None:
            last = last.next
        last.next = new_node
        new_node.prev = last
        self.size += 1
        return

    def listprint(self, node):
        while node is not None:
            print(node.data)
            node = node.next

    def remove(self, value):
        if self.head is None:
            print("Empty linked list")

        if self.head.data == value:
            self.head = self.head.next
            if self.head is not None:
                self.head.prev = None
            self.size -= 1
        else:
            temp = self.head
            while temp is not None and temp.data != value:
                temp = temp.next
            if temp is None:
                print("Deleted node is not found")
            else:
                temp.prev.next = temp.next
                if temp.next is not None:
                    temp.next.prev = temp.prev
                self.size -= 1


class stack:

    def __init__(self):
        self.head = None

    def push(self, new_data):
        if self.head is None:
            self.head = Node(new_data)
        else:
            new_node = Node(new_data)
            self.head.prev = new_node
            new_node.next = self.head
            self.head = new_node

    def pop(self):
        if self.head is None:
            return None
        elif self.head.next is None:
            temp_data = self.head.data
            self.head = None
            return temp_data
        else:
            temp_data = self.head.data
            self.head = self.head.next
            self.head.prev = None
            return temp_data

    def top(self):
        return self.head.data

    def isEmpty(self):
        if self.head is None:
            return True
        else:
            return False
