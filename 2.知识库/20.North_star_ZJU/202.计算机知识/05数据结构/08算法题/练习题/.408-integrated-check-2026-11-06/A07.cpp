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

int StableSetDifference(int A[], int n, const int B[], int m, int M) {
    int *seen = new int[M + 1]();
    for (int j = 0; j < m; j++) seen[B[j]] = 1;
    int w = 0;
    for (int r = 0; r < n; r++)
        if (seen[A[r]] == 0) A[w++] = A[r];
    delete[] seen;
    return w;
}
