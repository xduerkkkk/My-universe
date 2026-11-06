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

void DeleteAboveOriginalMean(LinkList L) {
    long long sum = 0, count = 0;
    for (LNode *p = L->next; p != NULL; p = p->next) {
        sum += p->data; count++;
    }
    LNode *pre = L, *p = L->next;
    while (p != NULL) {
        if ((long long)p->data * count > sum) {
            pre->next = p->next;
            delete p;
            p = pre->next;
        } else { pre = p; p = p->next; }
    }
}
