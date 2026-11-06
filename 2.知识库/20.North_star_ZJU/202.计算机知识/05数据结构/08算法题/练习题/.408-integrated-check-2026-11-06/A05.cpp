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

int FirstAtLeast(const int A[], int n, int x) {
    int low = 0, high = n - 1, answer = n;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (A[mid] >= x) { answer = mid; high = mid - 1; }
        else low = mid + 1;
    }
    return answer;
}
int FirstGreater(const int A[], int n, int x) {
    int low = 0, high = n - 1, answer = n;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (A[mid] > x) { answer = mid; high = mid - 1; }
        else low = mid + 1;
    }
    return answer;
}
int ValueRangeCount(const int A[], int n, int low, int high) {
    return FirstGreater(A, n, high) - FirstAtLeast(A, n, low);
}
