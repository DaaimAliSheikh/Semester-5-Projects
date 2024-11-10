import time
import tracemalloc


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, u):
        if u != self.parent[u]:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        rootU = self.find(u)
        rootV = self.find(v)
        if rootU != rootV:
            self.parent[rootU] = rootV
            return False  # No cycle was formed
        return True  # Cycle detected


def prims_algorithm(graph):
    nodes = len(graph)
    visited = [False] * nodes
    reachable = []
    mst_edges = []
    mst_cost = 0

    current = 0

    while True:
        visited[current] = True
        for i in range(nodes):
            if graph[current][i] != 0:
                reachable.append((current, i, graph[current][i]))

        min_edge_value = float('inf')
        min_reachable = -1
        for i in range(len(reachable)):
            u, v, weight = reachable[i]
            if not visited[v] and weight < min_edge_value:
                min_reachable = i
                min_edge_value = weight

        if min_reachable == -1:
            break

        u, v, weight = reachable[min_reachable]
        mst_edges.append((u, v, weight))
        mst_cost += weight
        current = v

    mst_matrix = [[0] * nodes for _ in range(nodes)]
    for u, v, weight in mst_edges:
        mst_matrix[u][v] = weight
        mst_matrix[v][u] = weight  # For undirected graph

    return {"mst_cost": mst_cost, "mst_edges": mst_edges, "mst_matrix": mst_matrix}


def kruskals_algorithm(graph):
    nodes = len(graph)
    edges = []

    for u in range(nodes):
        for v in range(u + 1, nodes):
            if graph[u][v] != 0:
                edges.append((u, v, graph[u][v]))

    edges.sort(key=lambda x: x[2])

    uf = UnionFind(nodes)
    mst_cost = 0
    mst_edges = []

    for u, v, weight in edges:
        if not uf.union(u, v):
            mst_cost += weight
            mst_edges.append((u, v, weight))

    mst_matrix = [[0] * nodes for _ in range(nodes)]
    for u, v, weight in mst_edges:
        mst_matrix[u][v] = weight
        mst_matrix[v][u] = weight

    return {"mst_cost": mst_cost, "mst_edges": mst_edges, "mst_matrix": mst_matrix}


def memory_in_mb(bytes_used):
    return round(bytes_used / (1024 * 1024), 4)


def benchmark_algorithm(algorithm, graph, label):
    tracemalloc.start()
    start_time = time.time()

    result = algorithm(graph)

    end_time = time.time()
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    time_taken = (end_time - start_time) * 1000  # Convert to milliseconds
    memory_used = memory_in_mb(peak_memory)

    print(f"{label} Results:")
    print(f"MST Cost: {result['mst_cost']}")
    print(f"Time Taken: {time_taken:.4f} ms")
    print(f"Memory Used: {memory_used} MB")
    print("Minimum Spanning Tree (MST) as 2D Matrix:")
    for row in result['mst_matrix']:
        print(row)
    print('----------------------------------------')
    return result, time_taken, memory_used


# Example Graphs
graph1 = [
    [0, 2, 0, 6, 0],
    [2, 0, 3, 8, 5],
    [0, 3, 0, 0, 7],
    [6, 8, 0, 0, 9],
    [0, 5, 7, 9, 0]
]

graph2 = [
    [0, 1, 4, 0, 0],
    [1, 0, 4, 2, 7],
    [4, 4, 0, 3, 5],
    [0, 2, 3, 0, 4],
    [0, 7, 5, 4, 0]
]

# Running and benchmarking the algorithms
print("===== Prim's Algorithm Benchmarks =====")
benchmark_algorithm(prims_algorithm, graph1, "Graph 1 - Prim's Algorithm")
benchmark_algorithm(prims_algorithm, graph2, "Graph 2 - Prim's Algorithm")

print("\n===== Kruskal's Algorithm Benchmarks =====")
benchmark_algorithm(kruskals_algorithm, graph1,
                    "Graph 1 - Kruskal's Algorithm")
benchmark_algorithm(kruskals_algorithm, graph2,
                    "Graph 2 - Kruskal's Algorithm")
