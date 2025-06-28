#include <stdio.h>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <omp.h>
#include <math.h>
#include <cstring>

using namespace std;

typedef unsigned short node_t;
typedef unsigned short degree_t;
typedef vector<vector<node_t>> adj_t;
typedef float (*costfn_t)(node_t, adj_t, vector<degree_t>);

// ==============
// Cost functions
// ==============
float uniformCost(node_t n, adj_t adj, vector<degree_t> nodesDegree) {
    return 1.f;
}

float degreeCost(node_t n, adj_t adj, vector<degree_t> nodesDegree) {
    return ceil((float)nodesDegree[n] / 2.f);
}

// ==============
// Seed set functions
// ==============
bool* costSeedsGreedy(node_t n, adj_t adj, vector<degree_t> nodesDegree, float k, costfn_t c) {
    bool* sP = new bool[n];
    bool* sD = new bool[n];
    #pragma omp parallel for
    for (node_t i = 0; i < n; i++) {
        sP[i] = 0;
        sD[i] = 0;
    }
    float seedSetCost = 0.f;
    const int numThreads = omp_get_max_threads();
    do {
        float fI = 0.f;
        #pragma omp parallel for schedule(dynamic) reduction(+:fI)
        for (node_t v = 0; v < n; v++) {
            degree_t nV = 0;
            for (const node_t& j : adj[v]) {
                nV += sD[j];
            }
            float b = ceil(nodesDegree[v] / 2);
            fI += nV < b ? nV : b;
        }

        node_t* us = new node_t[numThreads];
        float* uFactors = new float[numThreads];
        for (int i = 0; i < numThreads; i++) {
            us[i] = 0;
            uFactors[i] = 0.0f;
        }
        #pragma omp parallel for schedule(dynamic)
        for (node_t v = 0; v < n; v++) {
            if (!sD[v]) {
                int tid = omp_get_thread_num();

                float fIV = 0.0f;
                for (node_t i = 0; i < n; i++) {
                    degree_t nV = 0;
                    for (const node_t& j : adj[i]) {
                        nV += sD[j] || j == v;
                    }
                    float b = ceil(nodesDegree[i] / 2);
                    fIV += nV < b ? nV : b;
                }
                float deltaV = fIV - fI; // (1)
                float cV = c(v, adj, nodesDegree);
                float vFactor = deltaV / cV; // (1)

                if (vFactor > uFactors[tid]) {
                    us[tid] = v;
                    uFactors[tid] = vFactor;
                }
            }
        }
        node_t u = 0;
        float uFactor = 0.f;
        for (int i = 0; i < numThreads; i++) {
            if (uFactors[i] > uFactor) {
                uFactor = uFactors[i];
                u = us[i];
            }
        }
        // S_p = S_d; // (5)
        memcpy(sP, sD, n * sizeof(bool));
        // (6) S_d = S_p \cup \{u\}
        sD[u] = true;
        seedSetCost += c(u, adj, nodesDegree);
        printf("%d\n", u);
    } while(seedSetCost < k);
    printf("==============\n");
    printf("%f/%f\n", seedSetCost, k);
    return sP;
}

int main(int argc, char** argv) {

    // Argument count check
    if (argc != 5) {
        printf("Usage: %s <name> <num_threads> <degree|uniform> <k>\n", argv[0]);
        return 1;
    }

    int k = atoi(argv[4]);

    string costType = argv[3];
    costfn_t costFunction;
    if (costType == "uniform") {
        costFunction = uniformCost;
    } else if (costType == "degree") {
        costFunction = degreeCost;
    } else {
        printf("Error: Invalid cost function type '%s'. Use 'uniform' or 'degree'.\n", costType.c_str());
        return 1;
    }

    // Obtain the specified dataset path
    std::string datasetPath = argv[1];
    printf("Dataset path: %s\n", datasetPath.c_str());

    int num_threads = atoi(argv[2]);
    omp_set_num_threads(num_threads);
    printf("Number of threads: %d\n", num_threads);

    // Open the file
    ifstream file(datasetPath);
    if (!file) {
        printf("Error: Could not open file %s\n", datasetPath.c_str());
        return 1;
    }

    // Parse the dataset
    node_t n = 0;
    adj_t adj;
    vector<degree_t> nodesDegree;
    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        string is, js;
        getline(ss, is, ',');
        getline(ss, js, ',');
        node_t il = stol(is);
        node_t jl = stol(js);
        // Check if the adjacency list contains enough entries, otherwise resize it and the nodes degree vectors
        node_t requiredSize = max(il, jl) + 1;
        if (adj.size() < requiredSize) {
            adj.resize(requiredSize);
            nodesDegree.resize(requiredSize);
            n = requiredSize;
        }
        // Append i and j representations to the adjacency list of each other
        adj[il].push_back(jl);
        adj[jl].push_back(il);
        // Update the degrees of nodes i and j
        nodesDegree[il]++;
        nodesDegree[jl]++;
    }

    bool* seedSet = costSeedsGreedy(n, adj, nodesDegree, k, costFunction);
}
