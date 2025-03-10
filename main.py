from dfs import get_tsp_path
from graph import Graph
from collections import deque
from networkx import DiGraph as DisplayGraph
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


def reader():
    csv = pd.read_csv('./route.csv', names=['origin', 'destiny', 'weight'], skiprows=1)
    g = Graph()

    for _, row in csv.iterrows():
        origin, destiny, weight = row['origin'], row['destiny'], row['weight']
        g.add_vertex(origin)
        g.add_vertex(destiny)
        g.add_edge(origin, destiny, weight)

    return g

def display_graph(g: Graph, path: list):
    dg = DisplayGraph()
    dg.add_nodes_from(path)
    
    for i in range(len(path) - 1):
        city1 = path[i]
        city2 = path[i+1]
        
        weight = None
        for neighbor, w in g.get_neighbors(city1):
            if neighbor == city2:
                weight = w
                break
        
        if weight is not None:
            dg.add_edge(city1, city2, weight=weight)
    
    if len(path) > 1:
        last_city = path[-1]
        first_city = path[0]
        
        weight = None
        for neighbor, w in g.get_neighbors(last_city):
            if neighbor == first_city:
                weight = w
                break
        
        if weight is not None:
            dg.add_edge(last_city, first_city, weight=weight)

    plt.figure(figsize=(10, 8))
    pos = nx.shell_layout(dg)

    node_colors = ["skyblue" if node == path[0] else "lightgreen" for node in dg.nodes]

    nx.draw(dg, pos, with_labels=True, arrowsize=20, node_color=node_colors, 
            node_size=1000, font_size=8, font_weight='semibold', edge_color='gray')

    edge_labels = {(u, v): d["weight"] for u, v, d in dg.edges(data=True)}
    nx.draw_networkx_edge_labels(dg, pos, edge_labels=edge_labels, font_size=10, 
                                font_color="black", font_weight="semibold")

    plt.title("Visualização do Grafo - Caminho do Caixeiro Viajante (TSP)")
    plt.show()

if __name__ == "__main__":
    g = reader()

    starting = str(input("Escolha uma cidade de origem: ")).upper()

    result = get_tsp_path(g, starting)
    
    if result[1]:
        print(f"[TSP] Menor custo do circuito: {result[0]} KM")
        print(f"[TSP] Caminho: {' -> '.join(result[1])}")

        display_graph(g, result[1])
    else:
        print(f"[TSP] Nenhum circuito encontrado começando em {starting}")

