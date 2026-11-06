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

void CountComponent(const ALGraph &G, int v, int visited[],
                    int &vertexCount, int &degreeSum) {
    visited[v] = 1;
    vertexCount++;
    for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc) {
        degreeSum++;
        int w = p->adjvex;
        if (visited[w] == 0)
            CountComponent(G, w, visited, vertexCount, degreeSum);
    }
}

int TreeComponentCount(const ALGraph &G) {
    int n = G.vexnum;
    int *visited = new int[n]();
    int answer = 0;
    for (int v = 0; v < n; v++) {
        if (visited[v] == 0) {
            int vertexCount = 0, degreeSum = 0;
            CountComponent(G, v, visited, vertexCount, degreeSum);
            if (degreeSum / 2 == vertexCount - 1) answer++;
        }
    }
    delete[] visited;
    return answer;
}
