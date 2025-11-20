from collections import defaultdict

class Graph:

    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def DLS(self, src, target, maxDepth, depth=0, visited=None):
        if visited is None:
            visited = []

        visited.append(src)  # record visited node

        if src == target:
            return True, visited

        if maxDepth <= 0:
            return False, visited

        for i in self.graph[src]:
            found, visited = self.DLS(i, target, maxDepth - 1, depth + 1, visited)
            if found:
                return True, visited

        return False, visited

    def IDDFS(self, src, target, maxDepth):
        for i in range(maxDepth + 1):  # maxDepth included
            print(f"\nDepth Level {i}:")
            found, visited = self.DLS(src, target, i)
            print("Visited nodes so far:", " -> ".join(visited))
            if found:
                return True
        return False


# Create a graph with alphabet nodes
g = Graph(7)

g.addEdge('A', 'B')
g.addEdge('A', 'C')
g.addEdge('B', 'D')
g.addEdge('B', 'E')
g.addEdge('C', 'F')
g.addEdge('C', 'G')

target = 'G'
maxDepth = 3
src = 'A'

if g.IDDFS(src, target, maxDepth):
    print(f"\nTarget '{target}' is reachable from source '{src}' within max depth {maxDepth}")
else:
    print(f"\nTarget '{target}' is NOT reachable from source '{src}' within max depth {maxDepth}")
