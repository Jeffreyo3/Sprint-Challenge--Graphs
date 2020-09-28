# make Queue able to take in an initial value
# and add method to remove an item from queue out of order
class Queue():
    def __init__(self, arr = []):
        self.queue = arr
    def __str__(self):
        return f"{self.queue}"
    __repr__ = __str__
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)
    def delete(self, value):
        self.queue.remove(value)

# Add a method to return last item in list without pop()
class Stack():
    def __init__(self):
        self.stack = []
    def __str__(self):
        return f"{self.stack}"
    __repr__ = __str__
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)
    def last_item(self):
        return self.stack[-1]
