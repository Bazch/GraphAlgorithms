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
            yield current
            current = current.next

    def __reversed__(self):
        current = self.head
        while current.next is not None:
            current = current.next
        while current is not None:
            yield current
            current = current.prev

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
            print(node.data),
            last = node
            node = node.next

    def remove(self, removed_node):
        head_val = self.head
        if head_val is not None:
            if head_val.data == removed_node:
                self.head = head_val.next
                head_val = None
                self.size -= 1
                return
            while head_val is not None:
                if head_val.data == removed_node:
                    break
                prev = head_val
                head_val = head_val.next
            if head_val is None:
                return

            prev.next = head_val.next
            head_val.next.prev = head_val.prev
            head_val = None
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
