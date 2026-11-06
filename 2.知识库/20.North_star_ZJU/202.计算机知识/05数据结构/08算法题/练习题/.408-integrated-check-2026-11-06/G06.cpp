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

bool IsBipartite(const ALGraph &G) {
    int n = G.vexnum;
    int *color = new int[n](), *q = new int[n]();
    for (int v = 0; v < n; v++) color[v] = -1;
    bool ok = true;
    for (int start = 0; start < n && ok; start++) {
        if (color[start] != -1) continue;
        int front = 0, rear = 0;
        color[start] = 0; q[rear++] = start;
        while (front < rear && ok) {
            int v = q[front++];
            for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc) {
                int w = p->adjvex;
                if (color[w] == -1) { color[w] = 1 - color[v]; q[rear++] = w; }
                else if (color[w] == color[v]) { ok = false; break; }
            }
        }
    }
    delete[] color; delete[] q;
    return ok;
}
