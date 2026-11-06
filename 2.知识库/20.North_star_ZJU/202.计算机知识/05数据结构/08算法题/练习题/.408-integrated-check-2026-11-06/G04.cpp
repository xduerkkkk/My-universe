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

void BFSDistance(const ALGraph &G, int start, int dist[]) {
    int n = G.vexnum;
    int *q = new int[n]();
    for (int v = 0; v < n; v++) dist[v] = -1;
    int front = 0, rear = 0;
    dist[start] = 0;
    q[rear++] = start;
    while (front < rear) {
        int v = q[front++];
        for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc) {
            int w = p->adjvex;
            if (dist[w] == -1) {
                dist[w] = dist[v] + 1;
                q[rear++] = w;
            }
        }
    }
    delete[] q;
}

int ShortestPathVertices(const ALGraph &G, int start, int target, int out[]) {
    int n = G.vexnum;
    int *distStart = new int[n]();
    int *distTarget = new int[n]();
    BFSDistance(G, start, distStart);
    int count = 0;
    if (distStart[target] != -1) {
        BFSDistance(G, target, distTarget);
        for (int v = 0; v < n; v++) {
            if (distStart[v] != -1 && distTarget[v] != -1 &&
                distStart[v] + distTarget[v] == distStart[target])
                out[count++] = v;
        }
    }
    delete[] distStart;
    delete[] distTarget;
    return count;
}
