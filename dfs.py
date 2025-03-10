import time


def dfs_tsp(g, current, origin, visited, current_cost, current_path, min_result, all_cities):
    """Encontra o caminho de menor custo que passa por todas as cidades e volta à origem"""
    visited.add(current)
    current_path.append(current)
    
    # Se visitamos todas as cidades, tentamos voltar à origem
    if len(visited) == len(all_cities):
        for neighbor, weight in g.get_neighbors(current):
            if neighbor == origin:
                total_cost = current_cost + int(weight)
                if total_cost < min_result[0]:
                    min_result[0] = total_cost
                    min_result[1] = list(current_path) + [origin]
    else:
        # Continue visitando cidades não visitadas
        for neighbor, weight in g.get_neighbors(current):
            if neighbor not in visited:
                dfs_tsp(g, neighbor, origin, visited, current_cost + int(weight), 
                      current_path, min_result, all_cities)
    
    # Backtracking
    visited.remove(current)
    current_path.pop()

def get_tsp_path(g, origin):
    """Encontra o caminho mais curto do caixeiro viajante começando em origin"""
    # Coletar todas as cidades do grafo
    all_cities = set()
    for city in g.vertex_map.keys():
        all_cities.add(city)
    
    min_result = [float('inf'), []]  # [menor custo, caminho correspondente]
    
    start_time = time.perf_counter() 
    
    dfs_tsp(g, origin, origin, set(), 0, [], min_result, all_cities)
    
    end_time = time.perf_counter() 

    elapsed_time = end_time - start_time

    print(f"[TSP] Tempo de execução: {elapsed_time:.6f} segundos")


    return min_result