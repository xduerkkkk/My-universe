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

int ArrayIntersection(const int A[], int n, const int B[], int m, int out[]) {
    int i = 0, j = 0, k = 0;
    while (i < n && j < m) {
        if (A[i] < B[j]) i++;
        else if (A[i] > B[j]) j++;
        else {
            if (k == 0 || out[k - 1] != A[i]) out[k++] = A[i];
            i++; j++;
        }
    }
    return k;
}
