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

void CollectRange(BTNode *p, int low, int high, int result[], int &count) {
    if (p == NULL) return;
    if (p->data > low) CollectRange(p->lchild, low, high, result, count);
    if (p->data >= low && p->data <= high) {
        result[count] = p->data;
        count++;
    }
    if (p->data < high) CollectRange(p->rchild, low, high, result, count);
}

int BSTRange(BTNode *root, int low, int high, int result[]) {
    if (low > high) return 0;
    int count = 0;
    CollectRange(root, low, high, result, count);
    return count;
}
