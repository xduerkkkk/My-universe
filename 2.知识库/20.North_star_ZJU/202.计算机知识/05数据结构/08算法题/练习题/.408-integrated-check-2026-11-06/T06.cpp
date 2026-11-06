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

bool SearchSumPath(BTNode *p, long long K, long long sum, int out[], int &length) {
    if (p == NULL) return false;
    out[length++] = p->data;
    sum += p->data;
    if (p->lchild == NULL && p->rchild == NULL && sum == K) return true;
    if (SearchSumPath(p->lchild, K, sum, out, length) ||
        SearchSumPath(p->rchild, K, sum, out, length)) return true;
    length--;
    return false;
}
bool FindSumPath(BTNode *root, long long K, int out[], int &length) {
    length = 0;
    return SearchSumPath(root, K, 0, out, length);
}
