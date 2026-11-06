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

BTNode *ContractSingle(BTNode *p) {
    if (p == NULL) return NULL;
    p->lchild = ContractSingle(p->lchild);
    p->rchild = ContractSingle(p->rchild);
    if (p->lchild != NULL && p->rchild == NULL) {
        BTNode *child = p->lchild;
        delete p;
        return child;
    }
    if (p->lchild == NULL && p->rchild != NULL) {
        BTNode *child = p->rchild;
        delete p;
        return child;
    }
    return p;
}
