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

void ReverseDFS(const int A[][MAXSIZE], int n, int v, int visited[]) {
    visited[v] = 1;
    for (int u = 0; u < n; u++) {
        if (A[u][v] != 0 && visited[u] == 0)
            ReverseDFS(A, n, u, visited);
    }
}

int VerticesReachingTarget(const int A[][MAXSIZE], int n, int target,
                          int out[]) {
    int *visited = new int[n]();
    ReverseDFS(A, n, target, visited);
    int count = 0;
    for (int v = 0; v < n; v++)
        if (visited[v] != 0) out[count++] = v;
    delete[] visited;
    return count;
}
