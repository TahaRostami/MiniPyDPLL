class Heap:
    def __init__(self, comp):
        self.comp = comp
        self.heap = [-1]  # Initialize heap with -1 to match the 1-based indexing
        self.indices = []

    @staticmethod
    def left(i):
        return 2 * i

    @staticmethod
    def right(i):
        return 2 * i + 1

    @staticmethod
    def parent(i):
        return i // 2

    def percolate_up(self, i):
        x = self.heap[i]
        while self.parent(i) != 0 and self.comp(x, self.heap[self.parent(i)]):
            self.heap[i] = self.heap[self.parent(i)]
            self.indices[self.heap[i]] = i
            i = self.parent(i)
        self.heap[i] = x
        self.indices[x] = i

    def percolate_down(self, i):
        x = self.heap[i]
        while self.left(i) < len(self.heap):
            child = (self.right(i) < len(self.heap) and self.comp(self.heap[self.right(i)], self.heap[self.left(i)])) and self.right(i) or self.left(i)
            if not self.comp(self.heap[child], x):
                break
            self.heap[i] = self.heap[child]
            self.indices[self.heap[i]] = i
            i = child
        self.heap[i] = x
        self.indices[x] = i

    def ok(self, n):
        return 0 <= n < len(self.indices)

    def set_bounds(self, size):
        assert size >= 0
        self.indices = [0] * size

    def in_heap(self, n):
        assert self.ok(n)
        return self.indices[n] != 0

    def increase(self, n):
        assert self.ok(n)
        assert self.in_heap(n)
        self.percolate_up(self.indices[n])

    def empty(self):
        return len(self.heap) == 1

    def insert(self, n):
        assert self.ok(n)
        self.indices[n] = len(self.heap)
        self.heap.append(n)
        self.percolate_up(self.indices[n])

    def get_min(self):
        r = self.heap[1]
        self.heap[1] = self.heap[-1]
        self.indices[self.heap[1]] = 1
        self.indices[r] = 0
        self.heap.pop()
        if len(self.heap) > 1:
            self.percolate_down(1)
        return r

    def heap_property(self):
        return self.heap_property_helper(1)

    def heap_property_helper(self, i):
        return i >= len(self.heap) or (
            (self.parent(i) == 0 or not self.comp(self.heap[i], self.heap[self.parent(i)]))
            and self.heap_property_helper(self.left(i))
            and self.heap_property_helper(self.right(i))
        )
def int_less(a, b):
    return a < b