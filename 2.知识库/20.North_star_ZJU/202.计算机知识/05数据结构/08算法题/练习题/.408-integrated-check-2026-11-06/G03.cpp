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

int MinimumTerms(const ALGraph &G) {
    int n = G.vexnum;
    int *indegree = new int[n]();
    int *q = new int[n]();
    for (int v = 0; v < n; v++) {
        for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc)
            indegree[p->adjvex]++;
    }
    int front = 0, rear = 0;
    for (int v = 0; v < n; v++)
        if (indegree[v] == 0) q[rear++] = v;
    int terms = 0, processed = 0;
    while (front < rear) {
        int end = rear;
        terms++;
        while (front < end) {
            int v = q[front++];
            processed++;
            for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc) {
                int w = p->adjvex;
                indegree[w]--;
                if (indegree[w] == 0) q[rear++] = w;
            }
        }
    }
    delete[] indegree;
    delete[] q;
    if (processed < n) return -1;
    return terms;
}
