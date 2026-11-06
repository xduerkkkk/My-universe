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

void DFSIgnoring(const ALGraph &G, int v, int visited[]) {
    visited[v] = 1;
    for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc)
        if (visited[p->adjvex] == 0) DFSIgnoring(G, p->adjvex, visited);
}
int ComponentsWithoutVertex(const ALGraph &G, int blocked) {
    int *visited = new int[G.vexnum]();
    visited[blocked] = 1;
    int count = 0;
    for (int v = 0; v < G.vexnum; v++)
        if (visited[v] == 0) { DFSIgnoring(G, v, visited); count++; }
    delete[] visited;
    return count;
}
