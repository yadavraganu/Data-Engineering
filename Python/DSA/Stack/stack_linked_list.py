class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self, maxsize):
        self.head = None
        self.maxsize = maxsize
        self.top = -1

    def __iter__(self):
        current_node = self.head
        while current_node:
            yield current_node
            current_node = current_node.next


class Stack:
    def __init__(self, maxsize):
        self.sll = LinkedList(maxsize)

    def isempty(self):
        if self.sll.head is None:
            return True
        else:
            return False

    def isfull(self):
        if self.sll.top == self.sll.maxsize - 1:
            return True
        else:
            return False

    def __str__(self):
        return '->'.join([str(x.value) for x in self.sll])

    def push(self, value):
        if self.isempty():
            new_node = Node(value)
            self.sll.head = new_node
            self.sll.top += 1
        elif self.isfull():
            raise Exception('Stack is full')
        else:
            new_node = Node(value)
            new_node.next = self.sll.head
            self.sll.head = new_node
            self.sll.top += 1

    def pop(self):
        if self.isempty():
            raise Exception('Stack is empty')
        else:
            deleted_node = self.sll.head
            self.sll.head = self.sll.head.next
            self.sll.top -= 1
            return deleted_node.value

if __name__ =='__main__':
    s = Stack(3)
    s.push(2)
    s.push(3)
    s.push(5)
    print(s, s.sll.top, s.isfull(), s.isempty())
    print(s.pop())
    print(s.pop())
    print(s.pop())
    print(s, s.sll.top, s.isfull(), s.isempty())
