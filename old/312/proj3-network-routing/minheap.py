class MinHeap:
    def __init__(self, nodes):
        self.V = []
        self.make_queue(nodes)

    def make_queue(self, nodes):
        self.index_map = {}
        for node in nodes:
            self.insert(node)

    def insert(self, node):
        self.V.append(node)
        index = len(self.V)-1
        self.index_map[node.node_id] = index
        self.bubbleup(index)

    def bubbleup(self, index):
        if index == 0:
            return
        p = 0  # parent index
        if index % 2 == 0:
            p = (index-2)//2
        else:
            p = (index-1)//2

        if self.V[index].dist < self.V[p].dist:
            parent = self.V[p]
            child = self.V[index]
            self.V[p] = child  # swap child and parent positions
            self.index_map[child.node_id] = p
            self.V[index] = parent
            self.index_map[parent.node_id] = index
            self.bubbleup(p)

    def delete_min(self):
        if len(self.V) == 1:
            return self.V.pop()
        root = self.V[0]
        self.V[0] = self.V[-1]  # Replace root with last node in heap
        self.V.pop()  # Delete the last node
        del self.index_map[root.node_id]
        self.index_map[self.V[0].node_id] = 0
        index = 0
        self.sift_down(index)
        return root

    def sift_down(self, index):
        cl = 2*index + 1
        if cl < len(self.V):
            child_l = self.V[cl]
            min_index = cl
            cr = cl + 1
            if cr < len(self.V):
                child_r = self.V[cr]
                if child_r.dist < child_l.dist:
                    min_index = cr
            parent = self.V[index]
            child = self.V[min_index]
            if child.dist < parent.dist:
                self.V[index] = child
                self.index_map[child.node_id] = index
                self.V[min_index] = parent
                self.index_map[parent.node_id] = min_index
                self.sift_down(min_index)

    def decrease_key(self, node):
        index = self.index_map[node.node_id]
        self.bubbleup(index)
