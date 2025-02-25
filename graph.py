class Node:
    def __init__(self, vertex, weight):
        self.vertex = vertex
        self.weight = weight
        self.next = None

class List:
    def __init__(self):
        self.head = None

    def push(self, vertex, weight):
        new_node = Node(vertex, weight)
        new_node.next = self.head
        self.head = new_node

    def exists(self, vertex):
        temp = self.head
        while temp:
            if temp.vertex == vertex:
                return True
            temp = temp.next
        return False

    def print_list(self):
        temp = self.head
        output = []
        while temp:
            output.append(f"({temp.vertex}, {temp.weight})")
            temp = temp.next
        print(" => ".join(output) + " ]")

class Graph:
    def __init__(self):
        self.graph = []
        self.vertex_map = {} 
        self.num_vertices = 0

    def get_neighbors(self, vertex):
        if vertex not in self.vertex_map:
            print(f"[!] O vértice '{vertex}' não existe.")
            return []
        
        index = self.vertex_map[vertex]
        temp = self.graph[index].head
        neighbors = []

        while temp:
            neighbors.append((temp.vertex, temp.weight))
            temp = temp.next

        return neighbors

    def add_vertex(self, name):
        if name in self.vertex_map:
            return
        
        self.vertex_map[name] = self.num_vertices
        self.graph.append(List())
        self.num_vertices += 1

    def add_edge(self, vertex1, vertex2, weight):
        if vertex1 not in self.vertex_map or vertex2 not in self.vertex_map:
            print(f"[!] Um ou ambos os vértices ('{vertex1}', '{vertex2}') não existem.")
            return

        index1 = self.vertex_map[vertex1]
        index2 = self.vertex_map[vertex2]

        if self.graph[index1].exists(vertex2):
            print(f"[!] Uma aresta para ({vertex1}, {vertex2}) já existe.")
            return

        self.graph[index1].push(vertex2, weight)
        self.graph[index2].push(vertex1, weight)

    def show(self):
        for name, index in self.vertex_map.items():
            print(f"Vértice {name} [", end="")
            self.graph[index].print_list()