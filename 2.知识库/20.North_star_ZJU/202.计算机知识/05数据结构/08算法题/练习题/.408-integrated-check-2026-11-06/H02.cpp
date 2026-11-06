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

void SiftDownMin(int A[], int n, int i) {
    int x = A[i];
    for (int child = 2 * i + 1; child < n; child = 2 * i + 1) {
        if (child + 1 < n && A[child + 1] < A[child]) child++;
        if (x <= A[child]) break;
        A[i] = A[child]; i = child;
    }
    A[i] = x;
}
void LargestK(const int A[], int n, int k, int result[]) {
    if (k == 0) return;
    for (int i = 0; i < k; i++) result[i] = A[i];
    for (int i = k / 2 - 1; i >= 0; i--) SiftDownMin(result, k, i);
    for (int i = k; i < n; i++) {
        if (A[i] > result[0]) {
            result[0] = A[i];
            SiftDownMin(result, k, 0);
        }
    }
}
