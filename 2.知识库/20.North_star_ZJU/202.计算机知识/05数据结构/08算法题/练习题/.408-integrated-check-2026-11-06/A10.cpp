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

bool MaximumDrop(const int A[], int n, long long &answer) {
    if (n < 2) return false;
    int previousMax = A[0];
    answer = (long long)A[0] - A[1];
    for (int j = 1; j < n; j++) {
        long long candidate = (long long)previousMax - A[j];
        if (candidate > answer) answer = candidate;
        if (A[j] > previousMax) previousMax = A[j];
    }
    return true;
}
