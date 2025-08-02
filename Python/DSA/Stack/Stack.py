class ArrayStack:
    def __init__(self, maxsize):
        self.storage = [None] * maxsize
        self.maxsize = maxsize
        self.length = 0

    def isempty(self):
        if self.length == 0:
            return True
        else:
            return False

    def isfull(self):
        if self.length == self.maxsize:
            return True
        else:
            return False

    def push(self, value):
        if self.isfull():
            raise Exception("Stack is full")
        else:
            self.storage[self.length] = value
            self.length += 1
            return True

    def pop(self):
        if self.isempty():
            raise Exception("Stack is empty")
        else:
            val = self.storage[self.length - 1]
            self.storage[self.length - 1] = None
            self.length -= 1
            return val

    def top(self):
        if self.isempty():
            raise Exception("Stack is empty")
        else:
            return self.storage[self.length - 1]

    def __str__(self):
        return " ".join([str(x) for x in self.storage if x is not None])

    def __repr__(self):
        return f"ArrayStack({self.maxsize})"

    def __len__(self):
        return self.length

    def status(self):
        if self.isempty():
            print("Stack is empty")
        else:
            print(
                f"{'#'*20}\nCapacity => {self.maxsize}\nLength => {self.length}\nTopElement => {self.top()}\n{'#'*20}"
            )


if __name__ == "__main__":
    s = ArrayStack(3)
    s.status()
    s.push(2)
    s.push(1)
    s.push(3)
    s.status()
    print(s.pop())
    print(s.pop())
    print(s.pop())
    s.status()
