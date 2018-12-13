class Uarray:
    def __init__(self, nodes):
        self.V = []  # Main array
        for i in range(len(nodes)):
            self.V.append(nodes[i])

    # Does a simple scan across the array to find the smallest distance.
    def delete_min(self):
        min_index = 0
        for i in range(len(self.V)):
            if self.V[i].dist < self.V[min_index].dist:
                min_index = i
        
        return self.V.pop(min_index)

    # This is only here because it's called in computeShortestPaths.
    def decrease_key(self, node):
        pass
