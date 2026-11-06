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

int CollectBalancedCuts(BTNode *p, int n, int out[], int &count) {
    if (p == NULL) return 0;
    int leftSize = CollectBalancedCuts(p->lchild, n, out, count);
    int rightSize = CollectBalancedCuts(p->rchild, n, out, count);
    int size = leftSize + rightSize + 1;
    int outside = n - size;
    int largest = leftSize > rightSize ? leftSize : rightSize;
    if (outside > largest) largest = outside;
    if (largest <= n / 2) out[count++] = p->data;
    return size;
}

int BalancedCuts(BTNode *root, int n, int out[]) {
    int count = 0;
    CollectBalancedCuts(root, n, out, count);
    return count;
}
