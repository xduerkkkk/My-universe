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

int FindRoot(int parent[], int v) {
    if (parent[v] != v) parent[v] = FindRoot(parent, parent[v]);
    return parent[v];
}
int RedundantEdges(int n, const int edges[][2], int m) {
    int *parent = new int[n](), *size = new int[n]();
    for (int v = 0; v < n; v++) { parent[v] = v; size[v] = 1; }
    int answer = 0;
    for (int i = 0; i < m; i++) {
        int a = FindRoot(parent, edges[i][0]), b = FindRoot(parent, edges[i][1]);
        if (a == b) { answer++; continue; }
        if (size[a] < size[b]) { int temp = a; a = b; b = temp; }
        parent[b] = a;
        size[a] += size[b];
    }
    delete[] parent; delete[] size;
    return answer;
}
