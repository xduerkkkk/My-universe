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

int HeightForDiameter(BTNode *p, int &best) {
    if (p == NULL) return 0;
    int left = HeightForDiameter(p->lchild, best);
    int right = HeightForDiameter(p->rchild, best);
    if (left + right > best) best = left + right;
    return (left > right ? left : right) + 1;
}
int TreeDiameter(BTNode *root) {
    int best = 0;
    HeightForDiameter(root, best);
    return best;
}
