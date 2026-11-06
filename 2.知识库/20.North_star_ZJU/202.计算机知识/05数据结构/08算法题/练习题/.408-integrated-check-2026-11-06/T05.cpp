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

int BalancedHeight(BTNode *p) {
    if (p == NULL) return 0;
    int left = BalancedHeight(p->lchild);
    if (left == -1) return -1;
    int right = BalancedHeight(p->rchild);
    if (right == -1 || left - right > 1 || right - left > 1) return -1;
    return (left > right ? left : right) + 1;
}
bool TreeBalanced(BTNode *root, int &height) {
    height = BalancedHeight(root);
    return height != -1;
}
