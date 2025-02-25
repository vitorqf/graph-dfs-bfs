from graph import Graph
from collections import deque
from networkx import DiGraph as DisplayGraph
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


def bfs(g, origin, destiny):
    """Encontra o menor número de paradas entre duas cidades usando BFS"""
    if origin not in g.vertex_map or destiny not in g.vertex_map:
        print(f"[!] Origem '{origin}' ou destino '{destiny}' não existem.")
        return -1, []

    q = deque([origin])
    visited = list([origin])
    predecessors = {origin: None}

    while q:
        curr = q.popleft()

        if curr == destiny:
            path = []
            while curr is not None:
                path.append(curr)
                curr = predecessors[curr]
            path.reverse()
            return path

        for neighbor, _ in g.get_neighbors(curr):
            if neighbor not in visited:
                visited.append(neighbor)
                q.append(neighbor)
                predecessors[neighbor] = curr

    return -1, []


def dfs(g, origin, destiny, visited, current_cost, current_path, max_result):
    """Encontra o caminho de maior custo entre duas cidades usando DFS"""
    visited.add(origin)
    current_path.append(origin)

    if origin == destiny:
        if current_cost > max_result[0]:
            max_result[0] = current_cost
            max_result[1] = list(current_path)

    else:
        for neighbor, weight in g.get_neighbors(origin):
            if neighbor not in visited:
                dfs(g, neighbor, destiny, visited, current_cost + int(weight), current_path, max_result)

    visited.remove(origin)
    current_path.pop()


if __name__ == "__main__":
    csv = pd.read_csv('./path.csv', names=['origin', 'destiny', 'weight'], skiprows=1)
    g = Graph()
    dg = DisplayGraph()

    for _, row in csv.iterrows():
        origin, destiny, weight = row['origin'], row['destiny'], row['weight']
        dg.add_node(origin)
        dg.add_node(destiny)
        dg.add_edge(origin, destiny, weight=int(weight))
        g.add_vertex(origin)
        g.add_vertex(destiny)
        g.add_edge(origin, destiny, weight)

    starting = str(input("Escolha uma origem de A a M: ")).upper()
    ending = str(input("Escolha um destino de A a M: ")).upper()

    bfs_path = bfs(g, starting, ending)
    min_jumps = len(bfs_path) - 1
    if min_jumps != -1:
        print(f"[BFS] Menor número de paradas entre {starting} e {ending}: {min_jumps}")
        print(f"[BFS] Caminho: {' -> '.join(bfs_path)}")
    else:
        print(f"[BFS] Nenhum caminho encontrado entre {starting} e {ending}")

    max_result = [float('-inf'), []]  # [maior custo, caminho correspondente]
    dfs(g, starting, ending, set(), 0, [], max_result)

    if max_result[1]:
        print(f"[DFS] Maior custo acumulado entre {starting} e {ending}: {max_result[0]}")
        print(f"[DFS] Caminho: {' -> '.join(max_result[1])}")
    else:
        print(f"[DFS] Nenhum caminho encontrado entre {starting} e {ending}")

    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(dg, seed=420)

    nx.draw(dg, pos, with_labels=True, node_color='lightgreen', node_size=500, font_size=12, font_weight='bold', edge_color='gray')

    edge_labels = {(u, v): d["weight"] for u, v, d in dg.edges(data=True)}
    nx.draw_networkx_edge_labels(dg, pos, edge_labels=edge_labels, font_size=12, font_color="black", font_weight="bold")

    if len(bfs_path) > 1:
        bfs_edges = [(bfs_path[i], bfs_path[i + 1]) for i in range(len(bfs_path) - 1)]
        nx.draw_networkx_edges(dg, pos, edgelist=bfs_edges, edge_color='blue', width=2.5, alpha=0.7)

    if len(max_result[1]) > 1:
        dfs_edges = [(max_result[1][i], max_result[1][i + 1]) for i in range(len(max_result[1]) - 1)]
        nx.draw_networkx_edges(dg, pos, edgelist=dfs_edges, edge_color='red', width=2.5, alpha=0.7)

    plt.title("Visualização do Grafo - Cidades (BFS em azul, DFS em vermelho)")
    plt.show()
