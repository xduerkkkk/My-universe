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

void MissingAndRepeated(const int A[], int n, int M, int missing[], int &missingCount,
                        int repeated[], int &repeatedCount) {
    int *freq = new int[M + 1]();
    for (int i = 0; i < n; i++) freq[A[i]]++;
    missingCount = repeatedCount = 0;
    for (int v = 0; v <= M; v++) {
        if (freq[v] == 0) missing[missingCount++] = v;
        if (freq[v] >= 2) repeated[repeatedCount++] = v;
    }
    delete[] freq;
}
