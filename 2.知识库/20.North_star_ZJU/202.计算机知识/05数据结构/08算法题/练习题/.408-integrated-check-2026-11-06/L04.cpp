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

void StableThreeGroups(LinkList L, int x) {
    LNode *head[3] = {NULL, NULL, NULL};
    LNode *tail[3] = {NULL, NULL, NULL};
    LNode *p = L->next;
    while (p != NULL) {
        LNode *next = p->next;
        p->next = NULL;
        int group = p->data < x ? 0 : (p->data == x ? 1 : 2);
        if (head[group] == NULL) head[group] = p;
        else tail[group]->next = p;
        tail[group] = p;
        p = next;
    }
    LNode *last = L;
    for (int group = 0; group < 3; group++) {
        if (head[group] != NULL) {
            last->next = head[group];
            last = tail[group];
        }
    }
    last->next = NULL;
}
