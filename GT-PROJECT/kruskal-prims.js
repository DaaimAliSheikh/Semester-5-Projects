// Prim's Algorithm Implementation
function primsAlgorithm(graph) {
    const nodes = graph.length;
    const visited = new Array(nodes).fill(false);
    const reachable = []
    mstEdges = [];
    let mstCost = 0;

    let current =0;
   

    while(true){
        visited[current] = true;
        for (let i = 0; i < nodes; i++) {
            if( graph[current][i] !== 0){
                reachable.push([current, i, graph[current][i]]);
            }
        }
        let minEdgeValue =Infinity;
        let minReachable = -1;
        for (let i = 0; i < reachable.length; i++) {
            if(!visited[reachable[i][1]] && reachable[i][2] < minEdgeValue){
                minReachable = i;
                minEdgeValue = reachable[i][2];
            }
        }
        if(minReachable === -1){
            break;
        }
        
        mstEdges.push(reachable[minReachable]);
        mstCost += reachable[minReachable][2];
        current = reachable[minReachable][1];
        
    }

   
   // Initialize MST matrix with 0s
   const mstMatrix = Array.from({ length: nodes }, () => new Array(nodes).fill(0));

    // Populate MST matrix with edges and weights
    for (const [u, v, weight] of mstEdges) {
        mstMatrix[u][v] = weight;
        mstMatrix[v][u] = weight; // For undirected graph, mirror the edge
    }

    return { mstCost, mstEdges, mstMatrix };
}

// Kruskal's Algorithm Implementation
class UnionFind {
    constructor(n) {
        this.parent = Array.from({ length: n }, (_, i) => i);
    }

    find(u) {
        if (u !== this.parent[u]) {
            this.parent[u] = this.find(this.parent[u]);
        }
        return this.parent[u];///find the root of the disjoint component which the node belongs too
    }

    union(u, v) {
        // Find the roots of the sets containing 'u' and 'v'
        const rootU = this.find(u);
        const rootV = this.find(v);

        // If the roots are different, we can safely union the sets
        if (rootU !== rootV) {
            this.parent[rootU] = rootV;  // Make rootV the parent of rootU or vice versa doesnt matter
            return false;  // No cycle was formed
        }
        return true;  // A cycle is formed because u and v are already connected
    }
}

function kruskalsAlgorithm(graph) {
    const nodes = graph.length;
    const edges = [];

    // Collect all edges
    for (let u = 0; u < nodes; u++) {
        for (let v = u + 1; v < nodes; v++) {
            if (graph[u][v] !== 0) {
                edges.push([u, v, graph[u][v]]);
            }
        }
    }

    // Sort edges by weight
    edges.sort((a, b) => a[2] - b[2]);

    const uf = new UnionFind(nodes);
    let mstCost = 0;
    const mstEdges = [];

    // Process edges in order
    for (const [u, v, weight] of edges) {
        if (!uf.union(u, v)) {
            mstCost += weight;
            mstEdges.push([u, v, weight]); // Include weight here
        }
    }

    // Initialize MST matrix with 0s
    const mstMatrix = Array.from({ length: nodes }, () => new Array(nodes).fill(0));

    // Populate MST matrix with edges and weights
    for (const [u, v, weight] of mstEdges) {
        mstMatrix[u][v] = weight;
        mstMatrix[v][u] = weight; // For undirected graph, mirror the edge
    }

    return { mstCost, mstEdges, mstMatrix };
}


function memoryInMB(bytes) {
    return (bytes / (1024 * 1024)).toFixed(4); // Convert bytes to MB
}
// Benchmarking Function
function benchmarkAlgorithm(algorithm, graph, label) {
    const initialMemory = process.memoryUsage().heapUsed;
    const start = process.hrtime.bigint();

    const result = algorithm(graph);

    const end = process.hrtime.bigint();
    const finalMemory = process.memoryUsage().heapUsed;

    const timeTaken = Number(end - start) / 1e6; // Convert nanoseconds to milliseconds
    const memoryUsed = finalMemory - initialMemory; // Calculate memory difference

    console.log(`${label} Results:`);
    console.log(`MST Cost: ${result.mstCost}`);
    console.log(`Time Taken: ${timeTaken.toFixed(4)} ms`);
    console.log(`Memory Used: ${memoryInMB(memoryUsed)} MB`);
    console.log("Minimum Spanning Tree (MST) as 2D Matrix:");
   console.log(result.mstMatrix);
    console.log('----------------------------------------');
    return { result, timeTaken, memoryUsed };
}

// Example Graphs
const graph1 = [
    [0, 4, 7],
    [4, 0, 3],
    [7, 3, 0]
  ]

const graph2 = [
    [0, 1, 0, 6],
    [1, 0, 3, 0],
    [0, 3, 0, 8],
    [6, 0, 8, 0]
  ]

const graph3 = [
    [0, 2, 0, 5, 3],
    [2, 0, 1, 0, 4],
    [0, 1, 0, 0, 7],
    [5, 0, 0, 0, 9],
    [3, 4, 7, 9, 0]
  ]

// Running and benchmarking the algorithms
console.log("===== Prim's Algorithm Benchmarks =====");
benchmarkAlgorithm(primsAlgorithm, graph1, "Graph 1 - Prim's Algorithm");
benchmarkAlgorithm(primsAlgorithm, graph2, "Graph 2 - Prim's Algorithm");
benchmarkAlgorithm(primsAlgorithm, graph3, "Graph 3 - Prim's Algorithm");

console.log("\n===== Kruskal's Algorithm Benchmarks =====");
benchmarkAlgorithm(kruskalsAlgorithm, graph1, "Graph 1 - Kruskal's Algorithm");
benchmarkAlgorithm(kruskalsAlgorithm, graph2, "Graph 2 - Kruskal's Algorithm");
benchmarkAlgorithm(kruskalsAlgorithm, graph3, "Graph 3 - Kruskal's Algorithm");
