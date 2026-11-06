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

bool IsLinkedMinHeap(BTNode *root, int n) {
    if (root == NULL) return true;
    BTNode **q = new BTNode *[n]();
    int front = 0, rear = 0;
    bool gap = false, valid = true;
    q[rear++] = root;
    while (front < rear && valid) {
        BTNode *p = q[front++];
        BTNode *child[2] = {p->lchild, p->rchild};
        for (int i = 0; i < 2; i++) {
            if (child[i] == NULL) gap = true;
            else {
                if (gap || p->data > child[i]->data) {
                    valid = false;
                    break;
                }
                q[rear++] = child[i];
            }
        }
    }
    delete[] q;
    return valid;
}
