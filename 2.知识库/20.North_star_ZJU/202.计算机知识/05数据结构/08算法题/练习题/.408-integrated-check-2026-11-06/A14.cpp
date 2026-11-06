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

int LongestIncreasingRun(const int A[], int n, int &start) {
    if (n == 0) { start = -1; return 0; }
    int currentStart = 0, bestLength = 1;
    start = 0;
    for (int i = 1; i < n; i++) {
        if (A[i] <= A[i - 1]) currentStart = i;
        int length = i - currentStart + 1;
        if (length > bestLength) { bestLength = length; start = currentStart; }
    }
    return bestLength;
}
