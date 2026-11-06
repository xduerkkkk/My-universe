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

LNode *FirstSharedNode(LinkList A, LinkList B) {
    int n = 0, m = 0;
    for (LNode *p = A->next; p != NULL; p = p->next) n++;
    for (LNode *q = B->next; q != NULL; q = q->next) m++;
    LNode *p = A->next, *q = B->next;
    while (n > m) { p = p->next; n--; }
    while (m > n) { q = q->next; m--; }
    while (p != q) { p = p->next; q = q->next; }
    return p;
}
