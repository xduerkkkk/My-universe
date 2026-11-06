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

void ExtractLongestIncreasingRun(LinkList L, LinkList R) {
    if (L->next == NULL) return;
    LNode *currentPre = L, *bestPre = L, *bestTail = L->next;
    LNode *previous = L->next;
    int currentLength = 1, bestLength = 1;
    for (LNode *p = previous->next; p != NULL; p = p->next) {
        if (p->data > previous->data) currentLength++;
        else { currentPre = previous; currentLength = 1; }
        if (currentLength > bestLength) {
            bestLength = currentLength;
            bestPre = currentPre; bestTail = p;
        }
        previous = p;
    }
    R->next = bestPre->next;
    bestPre->next = bestTail->next;
    bestTail->next = NULL;
}
