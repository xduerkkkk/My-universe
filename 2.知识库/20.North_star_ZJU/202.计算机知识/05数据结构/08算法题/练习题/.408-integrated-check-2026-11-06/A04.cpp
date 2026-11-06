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

long long MinAbsoluteDifference(const int A[], int n, const int B[], int m) {
    int i = 0, j = 0;
    long long best = (long long)A[0] - B[0];
    if (best < 0) best = -best;
    while (i < n && j < m) {
        long long difference = (long long)A[i] - B[j];
        if (difference < 0) difference = -difference;
        if (difference < best) best = difference;
        if (best == 0) return 0;
        if (A[i] < B[j]) i++;
        else j++;
    }
    return best;
}
