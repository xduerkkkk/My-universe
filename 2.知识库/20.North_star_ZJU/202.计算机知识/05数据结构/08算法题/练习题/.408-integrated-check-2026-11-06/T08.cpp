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

void AdjacentGap(BTNode *p, bool &hasPrevious, int &previous,
                 bool &hasPair, long long &gap) {
    if (p == NULL) return;
    AdjacentGap(p->lchild, hasPrevious, previous, hasPair, gap);
    if (hasPrevious) {
        long long current = (long long)p->data - previous;
        if (!hasPair || current < gap) gap = current;
        hasPair = true;
    }
    previous = p->data;
    hasPrevious = true;
    AdjacentGap(p->rchild, hasPrevious, previous, hasPair, gap);
}
bool MinimumBSTGap(BTNode *root, long long &gap) {
    bool hasPrevious = false, hasPair = false;
    int previous = 0;
    gap = 0;
    AdjacentGap(root, hasPrevious, previous, hasPair, gap);
    return hasPair;
}
