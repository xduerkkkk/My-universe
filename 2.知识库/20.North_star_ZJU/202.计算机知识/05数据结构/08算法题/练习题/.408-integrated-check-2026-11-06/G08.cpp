#include <stdio.h>
#include <limits.h>
#define MAXSIZE 1000  // 固定数组的最大元素数；不是当前题目的 n

typedef struct LNode {
    int data;
    struct LNode *next;
} LNode, *LinkList;

typedef struct BTNode {
    int data;
    struct BTNode *lchild, *rchild;
} BTNode;

typedef struct ArcNode {
    int adjvex;                 // 这条边指向哪个顶点
    struct ArcNode *nextarc;    // 同一起点的下一条边
} ArcNode;

typedef struct VNode {
    int data;
    ArcNode *firstarc;          // 从这个顶点发出的第一条边
} VNode;

typedef struct ALGraph {
    VNode vertices[MAXSIZE];
    int vexnum, arcnum;         // 当前顶点数、边数
} ALGraph;

void DijkstraDistances(const int weight[][MAXSIZE], int n, int s, int dist[]) {
    const int INF = INT_MAX / 4;
    int *settled = new int[n]();
    for (int v = 0; v < n; v++) dist[v] = INF;
    dist[s] = 0;
    for (int step = 0; step < n; step++) {
        int u = -1;
        for (int v = 0; v < n; v++)
            if (!settled[v] && (u == -1 || dist[v] < dist[u])) u = v;
        if (u == -1 || dist[u] == INF) break;
        settled[u] = 1;
        for (int v = 0; v < n; v++) {
            if (!settled[v] && weight[u][v] < INF &&
                dist[u] + weight[u][v] < dist[v])
                dist[v] = dist[u] + weight[u][v];
        }
    }
    delete[] settled;
}
