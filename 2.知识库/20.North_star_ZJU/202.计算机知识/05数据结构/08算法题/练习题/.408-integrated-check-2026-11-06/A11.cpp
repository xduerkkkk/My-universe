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

void ThreeWayPartition(int A[], int n, int x, int &lessEnd, int &greaterStart) {
    int less = 0, i = 0, greater = n - 1;
    while (i <= greater) {
        if (A[i] < x) {
            int temp = A[i]; A[i] = A[less]; A[less] = temp;
            less++; i++;
        } else if (A[i] == x) i++;
        else {
            int temp = A[i]; A[i] = A[greater]; A[greater] = temp;
            greater--;
        }
    }
    lessEnd = less;
    greaterStart = greater + 1;
}
