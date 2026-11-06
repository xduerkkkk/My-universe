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

LNode *ReverseDataChain(LNode *p) {
    LNode *pre = NULL;
    while (p != NULL) {
        LNode *next = p->next;
        p->next = pre; pre = p; p = next;
    }
    return pre;
}
void ReorderEnds(LinkList L) {
    if (L->next == NULL || L->next->next == NULL) return;
    LNode *slow = L->next, *fast = L->next;
    while (fast->next != NULL && fast->next->next != NULL) {
        slow = slow->next; fast = fast->next->next;
    }
    LNode *second = slow->next;
    slow->next = NULL;
    LNode *p = L->next, *q = ReverseDataChain(second);
    while (q != NULL) {
        LNode *nextP = p->next, *nextQ = q->next;
        p->next = q; q->next = nextP;
        p = nextP; q = nextQ;
    }
}
