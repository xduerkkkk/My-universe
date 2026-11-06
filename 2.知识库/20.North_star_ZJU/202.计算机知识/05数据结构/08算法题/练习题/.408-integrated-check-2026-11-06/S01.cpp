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

bool BracketsMatch(const char A[], int n) {
    char *stack = new char[n]();
    int top = -1;
    bool ok = true;
    for (int i = 0; i < n && ok; i++) {
        char c = A[i];
        if (c == '(' || c == '[' || c == '{') stack[++top] = c;
        else {
            if (top == -1) { ok = false; break; }
            char left = stack[top--];
            if (!((left == '(' && c == ')') || (left == '[' && c == ']') ||
                  (left == '{' && c == '}'))) ok = false;
        }
    }
    ok = ok && top == -1;
    delete[] stack;
    return ok;
}
