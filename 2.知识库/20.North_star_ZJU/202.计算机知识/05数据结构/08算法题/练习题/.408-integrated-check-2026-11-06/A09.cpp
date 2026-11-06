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

int OrderedPivots(const int A[], int n, int out[]) {
    if (n < 3) return 0;
    int *rightMin = new int[n]();
    rightMin[n - 1] = A[n - 1];
    for (int i = n - 2; i >= 0; i--)
        rightMin[i] = A[i] < rightMin[i + 1] ? A[i] : rightMin[i + 1];
    int leftMax = A[0], count = 0;
    for (int i = 1; i + 1 < n; i++) {
        if (leftMax < A[i] && A[i] < rightMin[i + 1]) out[count++] = i;
        if (A[i] > leftMax) leftMax = A[i];
    }
    delete[] rightMin;
    return count;
}
