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

namespace A01 {
int DeleteValueRange(int A[], int n, int low, int high) {
    int w = 0;
    for (int r = 0; r < n; r++)
        if (A[r] < low || A[r] > high) A[w++] = A[r];
    return w;
}
}

namespace A02 {
int CompressCounts(int A[], int n, int counts[]) {
    int w = 0;
    for (int r = 0; r < n; r++) {
        if (w == 0 || A[r] != A[w - 1]) {
            A[w] = A[r];
            counts[w] = 1;
            w++;
        } else counts[w - 1]++;
    }
    return w;
}
}

namespace A03 {
int ArrayIntersection(const int A[], int n, const int B[], int m, int out[]) {
    int i = 0, j = 0, k = 0;
    while (i < n && j < m) {
        if (A[i] < B[j]) i++;
        else if (A[i] > B[j]) j++;
        else {
            if (k == 0 || out[k - 1] != A[i]) out[k++] = A[i];
            i++; j++;
        }
    }
    return k;
}
}

namespace A04 {
long long MinAbsoluteDifference(const int A[], int n, const int B[], int m) {
    int i = 0, j = 0;
    long long best = (long long)A[0] - B[0];
    if (best < 0) best = -best;
    while (i < n && j < m) {
        long long difference = (long long)A[i] - B[j];
        if (difference < 0) difference = -difference;
        if (difference < best) best = difference;
        if (best == 0) return 0;
        if (A[i] < B[j]) i++;
        else j++;
    }
    return best;
}
}

namespace A05 {
int FirstAtLeast(const int A[], int n, int x) {
    int low = 0, high = n - 1, answer = n;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (A[mid] >= x) { answer = mid; high = mid - 1; }
        else low = mid + 1;
    }
    return answer;
}
int FirstGreater(const int A[], int n, int x) {
    int low = 0, high = n - 1, answer = n;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (A[mid] > x) { answer = mid; high = mid - 1; }
        else low = mid + 1;
    }
    return answer;
}
int ValueRangeCount(const int A[], int n, int low, int high) {
    return FirstGreater(A, n, high) - FirstAtLeast(A, n, low);
}
}

namespace A06 {
void MissingAndRepeated(const int A[], int n, int M, int missing[], int &missingCount,
                        int repeated[], int &repeatedCount) {
    int *freq = new int[M + 1]();
    for (int i = 0; i < n; i++) freq[A[i]]++;
    missingCount = repeatedCount = 0;
    for (int v = 0; v <= M; v++) {
        if (freq[v] == 0) missing[missingCount++] = v;
        if (freq[v] >= 2) repeated[repeatedCount++] = v;
    }
    delete[] freq;
}
}

namespace A07 {
int StableSetDifference(int A[], int n, const int B[], int m, int M) {
    int *seen = new int[M + 1]();
    for (int j = 0; j < m; j++) seen[B[j]] = 1;
    int w = 0;
    for (int r = 0; r < n; r++)
        if (seen[A[r]] == 0) A[w++] = A[r];
    delete[] seen;
    return w;
}
}

namespace A08 {
int EqualSumCuts(const int A[], int n, int out[]) {
    long long total = 0, left = 0;
    for (int i = 0; i < n; i++) total += A[i];
    int count = 0;
    for (int i = 0; i + 1 < n; i++) {
        left += A[i];
        if (left == total - left) out[count++] = i;
    }
    return count;
}
}

namespace A09 {
int OrderedPivots(const int A[], int n, int out[]) {
    if (n < 3) return 0;
    int *rightMin = new int[n]();
    rightMin[n - 1] = A[n - 1];
    for (int i = n - 2; i >= 0; i--)
        rightMin[i] = A[i] < rightMin[i + 1] ? A[i] : rightMin[i + 1];
    int leftMax = A[0], count = 0;
    for (int i = 1; i + 1 < n; i++) {
        if (leftMax < A[i] && A[i] < rightMin[i + 1]) out[count++] = i;
        if (A[i] > leftMax) leftMax = A[i];
    }
    delete[] rightMin;
    return count;
}
}

namespace A10 {
bool MaximumDrop(const int A[], int n, long long &answer) {
    if (n < 2) return false;
    int previousMax = A[0];
    answer = (long long)A[0] - A[1];
    for (int j = 1; j < n; j++) {
        long long candidate = (long long)previousMax - A[j];
        if (candidate > answer) answer = candidate;
        if (A[j] > previousMax) previousMax = A[j];
    }
    return true;
}
}

namespace A11 {
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
}

namespace A12 {
int Partition(int A[], int low, int high) {
    int pivot = A[low];
    while (low < high) {
        while (low < high && A[high] >= pivot) high--;
        A[low] = A[high];
        while (low < high && A[low] <= pivot) low++;
        A[high] = A[low];
    }
    A[low] = pivot;
    return low;
}
void KeepSmallestK(int A[], int n, int k) {
    if (k == 0 || k == n) return;
    int low = 0, high = n - 1;
    while (low <= high) {
        int p = Partition(A, low, high);
        if (p == k - 1) return;
        if (p > k - 1) high = p - 1;
        else low = p + 1;
    }
}
}

namespace A13 {
int ShortestAtLeast(const int A[], int n, long long target) {
    int left = 0, best = n + 1;
    long long sum = 0;
    for (int right = 0; right < n; right++) {
        sum += A[right];
        while (sum >= target) {
            int length = right - left + 1;
            if (length < best) best = length;
            sum -= A[left++];
        }
    }
    return best == n + 1 ? 0 : best;
}
}

namespace A14 {
int LongestIncreasingRun(const int A[], int n, int &start) {
    if (n == 0) { start = -1; return 0; }
    int currentStart = 0, bestLength = 1;
    start = 0;
    for (int i = 1; i < n; i++) {
        if (A[i] <= A[i - 1]) currentStart = i;
        int length = i - currentStart + 1;
        if (length > bestLength) { bestLength = length; start = currentStart; }
    }
    return bestLength;
}
}

namespace A15 {
long long TightTriples(const int A[], int n, long long C) {
    int left = 0;
    long long answer = 0;
    for (int right = 0; right < n; right++) {
        while ((long long)A[right] - A[left] > C) left++;
        long long count = right - left;
        answer += count * (count - 1) / 2;
    }
    return answer;
}
}

namespace G01 {
void CountComponent(const ALGraph &G, int v, int visited[],
                    int &vertexCount, int &degreeSum) {
    visited[v] = 1;
    vertexCount++;
    for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc) {
        degreeSum++;
        int w = p->adjvex;
        if (visited[w] == 0)
            CountComponent(G, w, visited, vertexCount, degreeSum);
    }
}

int TreeComponentCount(const ALGraph &G) {
    int n = G.vexnum;
    int *visited = new int[n]();
    int answer = 0;
    for (int v = 0; v < n; v++) {
        if (visited[v] == 0) {
            int vertexCount = 0, degreeSum = 0;
            CountComponent(G, v, visited, vertexCount, degreeSum);
            if (degreeSum / 2 == vertexCount - 1) answer++;
        }
    }
    delete[] visited;
    return answer;
}
}

namespace G02 {
void ReverseDFS(const int A[][MAXSIZE], int n, int v, int visited[]) {
    visited[v] = 1;
    for (int u = 0; u < n; u++) {
        if (A[u][v] != 0 && visited[u] == 0)
            ReverseDFS(A, n, u, visited);
    }
}

int VerticesReachingTarget(const int A[][MAXSIZE], int n, int target,
                          int out[]) {
    int *visited = new int[n]();
    ReverseDFS(A, n, target, visited);
    int count = 0;
    for (int v = 0; v < n; v++)
        if (visited[v] != 0) out[count++] = v;
    delete[] visited;
    return count;
}
}

namespace G03 {
int MinimumTerms(const ALGraph &G) {
    int n = G.vexnum;
    int *indegree = new int[n]();
    int *q = new int[n]();
    for (int v = 0; v < n; v++) {
        for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc)
            indegree[p->adjvex]++;
    }
    int front = 0, rear = 0;
    for (int v = 0; v < n; v++)
        if (indegree[v] == 0) q[rear++] = v;
    int terms = 0, processed = 0;
    while (front < rear) {
        int end = rear;
        terms++;
        while (front < end) {
            int v = q[front++];
            processed++;
            for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc) {
                int w = p->adjvex;
                indegree[w]--;
                if (indegree[w] == 0) q[rear++] = w;
            }
        }
    }
    delete[] indegree;
    delete[] q;
    if (processed < n) return -1;
    return terms;
}
}

namespace G04 {
void BFSDistance(const ALGraph &G, int start, int dist[]) {
    int n = G.vexnum;
    int *q = new int[n]();
    for (int v = 0; v < n; v++) dist[v] = -1;
    int front = 0, rear = 0;
    dist[start] = 0;
    q[rear++] = start;
    while (front < rear) {
        int v = q[front++];
        for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc) {
            int w = p->adjvex;
            if (dist[w] == -1) {
                dist[w] = dist[v] + 1;
                q[rear++] = w;
            }
        }
    }
    delete[] q;
}

int ShortestPathVertices(const ALGraph &G, int start, int target, int out[]) {
    int n = G.vexnum;
    int *distStart = new int[n]();
    int *distTarget = new int[n]();
    BFSDistance(G, start, distStart);
    int count = 0;
    if (distStart[target] != -1) {
        BFSDistance(G, target, distTarget);
        for (int v = 0; v < n; v++) {
            if (distStart[v] != -1 && distTarget[v] != -1 &&
                distStart[v] + distTarget[v] == distStart[target])
                out[count++] = v;
        }
    }
    delete[] distStart;
    delete[] distTarget;
    return count;
}
}

namespace G05 {
void DFSIgnoring(const ALGraph &G, int v, int visited[]) {
    visited[v] = 1;
    for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc)
        if (visited[p->adjvex] == 0) DFSIgnoring(G, p->adjvex, visited);
}
int ComponentsWithoutVertex(const ALGraph &G, int blocked) {
    int *visited = new int[G.vexnum]();
    visited[blocked] = 1;
    int count = 0;
    for (int v = 0; v < G.vexnum; v++)
        if (visited[v] == 0) { DFSIgnoring(G, v, visited); count++; }
    delete[] visited;
    return count;
}
}

namespace G06 {
bool IsBipartite(const ALGraph &G) {
    int n = G.vexnum;
    int *color = new int[n](), *q = new int[n]();
    for (int v = 0; v < n; v++) color[v] = -1;
    bool ok = true;
    for (int start = 0; start < n && ok; start++) {
        if (color[start] != -1) continue;
        int front = 0, rear = 0;
        color[start] = 0; q[rear++] = start;
        while (front < rear && ok) {
            int v = q[front++];
            for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc) {
                int w = p->adjvex;
                if (color[w] == -1) { color[w] = 1 - color[v]; q[rear++] = w; }
                else if (color[w] == color[v]) { ok = false; break; }
            }
        }
    }
    delete[] color; delete[] q;
    return ok;
}
}

namespace G07 {
int FindRoot(int parent[], int v) {
    if (parent[v] != v) parent[v] = FindRoot(parent, parent[v]);
    return parent[v];
}
int RedundantEdges(int n, const int edges[][2], int m) {
    int *parent = new int[n](), *size = new int[n]();
    for (int v = 0; v < n; v++) { parent[v] = v; size[v] = 1; }
    int answer = 0;
    for (int i = 0; i < m; i++) {
        int a = FindRoot(parent, edges[i][0]), b = FindRoot(parent, edges[i][1]);
        if (a == b) { answer++; continue; }
        if (size[a] < size[b]) { int temp = a; a = b; b = temp; }
        parent[b] = a;
        size[a] += size[b];
    }
    delete[] parent; delete[] size;
    return answer;
}
}

namespace G08 {
void DijkstraDistances(const int weight[][MAXSIZE], int n, int s, int dist[]) {
    const int INF = INT_MAX / 4;
    int *settled = new int[n]();
    for (int v = 0; v < n; v++) dist[v] = INF;
    dist[s] = 0;
    for (int step = 0; step < n; step++) {
        int u = -1;
        for (int v = 0; v < n; v++)
            if (!settled[v] && (u == -1 || dist[v] < dist[u])) u = v;
        if (u == -1 || dist[u] == INF) break;
        settled[u] = 1;
        for (int v = 0; v < n; v++) {
            if (!settled[v] && weight[u][v] < INF &&
                dist[u] + weight[u][v] < dist[v])
                dist[v] = dist[u] + weight[u][v];
        }
    }
    delete[] settled;
}
}

namespace H01 {
void SiftDownMax(int A[], int n, int i) {
    int x = A[i];
    for (int child = 2 * i + 1; child < n; child = 2 * i + 1) {
        if (child + 1 < n && A[child + 1] > A[child]) child++;
        if (x >= A[child]) break;
        A[i] = A[child]; i = child;
    }
    A[i] = x;
}
void BuildMaxHeap(int A[], int n) {
    for (int i = n / 2 - 1; i >= 0; i--) SiftDownMax(A, n, i);
}
void HeapSort(int A[], int n) {
    BuildMaxHeap(A, n);
    for (int end = n - 1; end > 0; end--) {
        int temp = A[0]; A[0] = A[end]; A[end] = temp;
        SiftDownMax(A, end, 0);
    }
}
}

namespace H02 {
void SiftDownMin(int A[], int n, int i) {
    int x = A[i];
    for (int child = 2 * i + 1; child < n; child = 2 * i + 1) {
        if (child + 1 < n && A[child + 1] < A[child]) child++;
        if (x <= A[child]) break;
        A[i] = A[child]; i = child;
    }
    A[i] = x;
}
void LargestK(const int A[], int n, int k, int result[]) {
    if (k == 0) return;
    for (int i = 0; i < k; i++) result[i] = A[i];
    for (int i = k / 2 - 1; i >= 0; i--) SiftDownMin(result, k, i);
    for (int i = k; i < n; i++) {
        if (A[i] > result[0]) {
            result[0] = A[i];
            SiftDownMin(result, k, 0);
        }
    }
}
}

namespace L01 {
void ReverseList(LinkList L) {
    LNode *pre = NULL, *p = L->next;
    while (p != NULL) {
        LNode *next = p->next;
        p->next = pre;
        pre = p;
        p = next;
    }
    L->next = pre;
}
}

namespace L02 {
void MergeSortedLists(LinkList A, LinkList B) {
    LNode *p = A->next, *q = B->next, *tail = A;
    A->next = B->next = NULL;
    while (p != NULL && q != NULL) {
        if (p->data <= q->data) { tail->next = p; p = p->next; }
        else { tail->next = q; q = q->next; }
        tail = tail->next;
    }
    tail->next = p != NULL ? p : q;
}
}

namespace L03 {
void SubtractSortedList(LinkList A, LinkList B) {
    LNode *pre = A, *p = A->next, *q = B->next;
    while (p != NULL) {
        while (q != NULL && q->data < p->data) q = q->next;
        if (q != NULL && q->data == p->data) {
            pre->next = p->next;
            delete p;
            p = pre->next;
        } else { pre = p; p = p->next; }
    }
}
}

namespace L04 {
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
}

namespace L05 {
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
}

namespace L06 {
void SwapAdjacentNodes(LinkList L) {
    LNode *pre = L;
    while (pre->next != NULL && pre->next->next != NULL) {
        LNode *a = pre->next, *b = a->next;
        a->next = b->next;
        b->next = a;
        pre->next = b;
        pre = a;
    }
}
}

namespace L07 {
LNode *ReverseDataChain(LNode *p) {
    LNode *pre = NULL;
    while (p != NULL) {
        LNode *next = p->next;
        p->next = pre; pre = p; p = next;
    }
    return pre;
}
bool IsPalindromeRestore(LinkList L) {
    if (L->next == NULL || L->next->next == NULL) return true;
    LNode *slow = L->next, *fast = L->next;
    while (fast->next != NULL && fast->next->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;
    }
    LNode *second = ReverseDataChain(slow->next);
    slow->next = second;
    LNode *p = L->next, *q = second;
    bool ok = true;
    while (q != NULL) {
        if (p->data != q->data) ok = false;
        p = p->next; q = q->next;
    }
    slow->next = ReverseDataChain(second);
    return ok;
}
}

namespace L08 {
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
}

namespace L09 {
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
}

namespace L10 {
void AppendReversedCopy(LinkList L) {
    LNode *copyHead = NULL, *tail = L;
    for (LNode *p = L->next; p != NULL; p = p->next) {
        LNode *copy = new LNode{p->data, copyHead};
        copyHead = copy;
        tail = p;
    }
    tail->next = copyHead;
}
}

namespace L11 {
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
}

namespace S01 {
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
}

namespace S02 {
bool EvaluatePostfix(const char A[], int n, int &answer) {
    int *stack = new int[n]();
    int top = -1;
    bool ok = true;
    for (int i = 0; i < n && ok; i++) {
        char c = A[i];
        if (c >= '0' && c <= '9') stack[++top] = c - '0';
        else if (c == '+' || c == '-' || c == '*') {
            if (top < 1) { ok = false; break; }
            int right = stack[top--], left = stack[top--];
            int value = c == '+' ? left + right : (c == '-' ? left - right : left * right);
            stack[++top] = value;
        } else ok = false;
    }
    ok = ok && top == 0;
    if (ok) answer = stack[0];
    delete[] stack;
    return ok;
}
}

namespace T01 {
BTNode *ContractSingle(BTNode *p) {
    if (p == NULL) return NULL;
    p->lchild = ContractSingle(p->lchild);
    p->rchild = ContractSingle(p->rchild);
    if (p->lchild != NULL && p->rchild == NULL) {
        BTNode *child = p->lchild;
        delete p;
        return child;
    }
    if (p->lchild == NULL && p->rchild != NULL) {
        BTNode *child = p->rchild;
        delete p;
        return child;
    }
    return p;
}
}

namespace T02 {
typedef struct CSNode {
    int data;
    struct CSNode *firstchild, *nextsibling;
} CSNode;

long long LeafDepthSum(CSNode *p, int depth) {
    if (p == NULL) return 0;
    if (p->firstchild == NULL) return depth;
    long long sum = 0;
    for (CSNode *child = p->firstchild; child != NULL;
         child = child->nextsibling)
        sum += LeafDepthSum(child, depth + 1);
    return sum;
}
}

namespace T03 {
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
}

namespace T04 {
int CollectBalancedCuts(BTNode *p, int n, int out[], int &count) {
    if (p == NULL) return 0;
    int leftSize = CollectBalancedCuts(p->lchild, n, out, count);
    int rightSize = CollectBalancedCuts(p->rchild, n, out, count);
    int size = leftSize + rightSize + 1;
    int outside = n - size;
    int largest = leftSize > rightSize ? leftSize : rightSize;
    if (outside > largest) largest = outside;
    if (largest <= n / 2) out[count++] = p->data;
    return size;
}

int BalancedCuts(BTNode *root, int n, int out[]) {
    int count = 0;
    CollectBalancedCuts(root, n, out, count);
    return count;
}
}

namespace T05 {
int BalancedHeight(BTNode *p) {
    if (p == NULL) return 0;
    int left = BalancedHeight(p->lchild);
    if (left == -1) return -1;
    int right = BalancedHeight(p->rchild);
    if (right == -1 || left - right > 1 || right - left > 1) return -1;
    return (left > right ? left : right) + 1;
}
bool TreeBalanced(BTNode *root, int &height) {
    height = BalancedHeight(root);
    return height != -1;
}
}

namespace T06 {
bool SearchSumPath(BTNode *p, long long K, long long sum, int out[], int &length) {
    if (p == NULL) return false;
    out[length++] = p->data;
    sum += p->data;
    if (p->lchild == NULL && p->rchild == NULL && sum == K) return true;
    if (SearchSumPath(p->lchild, K, sum, out, length) ||
        SearchSumPath(p->rchild, K, sum, out, length)) return true;
    length--;
    return false;
}
bool FindSumPath(BTNode *root, long long K, int out[], int &length) {
    length = 0;
    return SearchSumPath(root, K, 0, out, length);
}
}

namespace T07 {
bool MirrorEqual(BTNode *a, BTNode *b) {
    if (a == NULL && b == NULL) return true;
    if (a == NULL || b == NULL) return false;
    return a->data == b->data &&
           MirrorEqual(a->lchild, b->rchild) &&
           MirrorEqual(a->rchild, b->lchild);
}
}

namespace T08 {
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
}

namespace T09 {
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
}

namespace T10 {
bool BSTFloor(BTNode *root, int x, int &answer) {
    bool found = false;
    BTNode *p = root;
    while (p != NULL) {
        if (p->data > x) p = p->lchild;
        else {
            answer = p->data; found = true;
            p = p->rchild;
        }
    }
    return found;
}
}

using namespace A01;
using namespace A02;
using namespace A03;
using namespace A04;
using namespace A05;
using namespace A06;
using namespace A07;
using namespace A08;
using namespace A09;
using namespace A10;
using namespace A11;
using namespace A12;
using namespace A13;
using namespace A14;
using namespace A15;
using namespace G01;
using namespace G02;
using namespace G03;
using namespace G04;
using namespace G05;
using namespace G06;
using namespace G07;
using namespace G08;
using namespace H01;
using namespace H02;
using namespace L01;
using namespace L02;
using namespace L03;
using namespace L04;
using namespace L05;
using namespace L06;
using namespace L07;
using namespace L08;
using namespace L09;
using namespace L10;
using namespace L11;
using namespace S01;
using namespace S02;
using namespace T01;
using namespace T02;
using namespace T03;
using namespace T04;
using namespace T05;
using namespace T06;
using namespace T07;
using namespace T08;
using namespace T09;
using namespace T10;
#include <algorithm>
#include <cassert>
#include <iostream>
#include <map>
#include <queue>
#include <random>
#include <set>
#include <utility>
#include <vector>
using namespace std;
mt19937 rng(20261106);
int pick(int n) { return static_cast<int>(rng() % n); }
using Matrix=vector<vector<int>>;
long long treeRounds=0,undirectedRounds=0,directedRounds=0;

void DestroyTree(BTNode *p) {
    if(p==NULL) return;
    DestroyTree(p->lchild); DestroyTree(p->rchild); delete p;
}
BTNode *MakeTree(const vector<int>& left,const vector<int>& right,const vector<int>& val,int v) {
    if(v<0) return NULL;
    return new BTNode{val[v],MakeTree(left,right,val,left[v]),MakeTree(left,right,val,right[v])};
}
void GetNodes(BTNode *p, map<int,BTNode*>& nodes) {
    if(!p) return;
    assert(!nodes.count(p->data)); nodes[p->data]=p;
    GetNodes(p->lchild,nodes); GetNodes(p->rchild,nodes);
}
int ContractOracle(int v,const vector<int>& left,const vector<int>& right,
                   map<int,pair<int,int>>& expected) {
    if(v<0) return -1;
    int l=ContractOracle(left[v],left,right,expected);
    int r=ContractOracle(right[v],left,right,expected);
    if(l<0 && r>=0) return r;
    if(l>=0 && r<0) return l;
    expected[v]={l,r}; return v;
}
bool HeapOracle(BTNode* root,int n) {
    queue<pair<BTNode*,unsigned long long>> q;
    if(root) q.push({root,1});
    bool ok=true;
    while(!q.empty()) {
        auto [p,pos]=q.front();q.pop();
        if(pos>static_cast<unsigned long long>(n)) ok=false;
        if(p->lchild) { if(p->data>p->lchild->data) ok=false; q.push({p->lchild,2*pos}); }
        if(p->rchild) { if(p->data>p->rchild->data) ok=false; q.push({p->rchild,2*pos+1}); }
    }
    return ok;
}
vector<int> CutOracle(const vector<int>& left,const vector<int>& right) {
    int n=static_cast<int>(left.size()); Matrix a(n,vector<int>(n));
    for(int i=0;i<n;i++) for(int j:{left[i],right[i]}) if(j>=0) a[i][j]=a[j][i]=1;
    vector<int> result;
    for(int removed=0;removed<n;removed++) {
        vector<int> seen(n);seen[removed]=1;int largest=0;
        for(int v=0;v<n;v++) if(!seen[v]) {
            queue<int> q;q.push(v);seen[v]=1;int size=0;
            while(!q.empty()) {int u=q.front();q.pop();size++;
                for(int w=0;w<n;w++) if(a[u][w]&&!seen[w]){seen[w]=1;q.push(w);}
            }
            largest=max(largest,size);
        }
        if(largest<=n/2) result.push_back(removed);
    }
    return result;
}
void TestTree(const vector<int>& left,const vector<int>& right) {
    int n=static_cast<int>(left.size()); vector<int> ids(n);for(int i=0;i<n;i++)ids[i]=i;
    BTNode* root=MakeTree(left,right,ids,n?0:-1);
    map<int,BTNode*> addresses;GetNodes(root,addresses);
    int out[MAXSIZE];int count=BalancedCuts(root,n,out);
    vector<int> actual(out,out+count);sort(actual.begin(),actual.end());
    assert(actual==CutOracle(left,right));
    map<int,pair<int,int>> expected;int expectedRoot=n?ContractOracle(0,left,right,expected):-1;
    root=ContractSingle(root);
    assert((root?root->data:-1)==expectedRoot);
    map<int,BTNode*> after;GetNodes(root,after);assert(after.size()==expected.size());
    for(auto [v,children]:expected) {
        assert(after.count(v)&&after[v]==addresses[v]);
        assert((after[v]->lchild?after[v]->lchild->data:-1)==children.first);
        assert((after[v]->rchild?after[v]->rchild->data:-1)==children.second);
    }
    DestroyTree(root);
    vector<int> values(n);for(int &v:values)v=pick(13)-6;
    root=MakeTree(left,right,values,n?0:-1);
    assert(IsLinkedMinHeap(root,n)==HeapOracle(root,n));
    DestroyTree(root);treeRounds++;
}
void TreeTests() {
    TestTree({},{});
    TestTree({-1},{-1});
    for(int n=1;n<=24;n++) {
        vector<int> l(n,-1),r(n,-1);
        for(int i=0;i+1<n;i++) l[i]=i+1;
        TestTree(l,r);
        fill(l.begin(),l.end(),-1);for(int i=0;i+1<n;i++)r[i]=i+1;TestTree(l,r);
        fill(r.begin(),r.end(),-1);
        for(int i=0;i<n;i++){if(2*i+1<n)l[i]=2*i+1; if(2*i+2<n)r[i]=2*i+2;}
        TestTree(l,r);
        vector<int> values(n);for(int i=0;i<n;i++)values[i]=i/2-5;
        BTNode* heap=MakeTree(l,r,values,0);assert(IsLinkedMinHeap(heap,n));DestroyTree(heap);
    }
    for(int rep=0;rep<2000;rep++) {
        int n=1+pick(24);vector<int> l(n,-1),r(n,-1);vector<pair<int,int>> slots={{0,0},{0,1}};
        for(int i=1;i<n;i++) {int k=pick(static_cast<int>(slots.size()));auto [p,s]=slots[k];
            slots[k]=slots.back();slots.pop_back(); (s? r[p]:l[p])=i;
            slots.push_back({i,0});slots.push_back({i,1});
        }
        TestTree(l,r);
    }
    assert(LeafDepthSum(NULL,0)==0);
    for(int rep=0;rep<1500;rep++) {
        int n=1+pick(80); vector<CSNode*> nodes;vector<int> depth(n),children(n);
        for(int i=0;i<n;i++)nodes.push_back(new CSNode{i,NULL,NULL});
        for(int i=1;i<n;i++) {int p=rep%3==0?0:rep%3==1?i-1:pick(i);depth[i]=depth[p]+1;children[p]++;
            nodes[i]->nextsibling=nodes[p]->firstchild;nodes[p]->firstchild=nodes[i];}
        long long expected=0;for(int i=0;i<n;i++)if(children[i]==0)expected+=depth[i];
        assert(LeafDepthSum(nodes[0],0)==expected);for(auto p:nodes)delete p;
    }
    cout<<"tree structural rounds: "<<treeRounds<<"; child-sibling rounds: 1500\n";
}

ALGraph MakeGraph(const Matrix&a) {
    ALGraph g{};g.vexnum=static_cast<int>(a.size());
    for(int u=0;u<g.vexnum;u++)for(int v=0;v<g.vexnum;v++)if(a[u][v]) {
        g.vertices[u].firstarc=new ArcNode{v,g.vertices[u].firstarc};g.arcnum++;
    }
    return g;
}
void DestroyGraph(ALGraph&g) {
    for(int i=0;i<g.vexnum;i++) {ArcNode*p=g.vertices[i].firstarc;
        while(p){ArcNode*next=p->nextarc;delete p;p=next;}g.vertices[i].firstarc=NULL;}
}
Matrix Distances(const Matrix&a) {
    int n=static_cast<int>(a.size());Matrix d(n,vector<int>(n,10000));
    for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(a[i][j])d[i][j]=1;
    for(int i=0;i<n;i++)d[i][i]=0;
    for(int k=0;k<n;k++)for(int i=0;i<n;i++)for(int j=0;j<n;j++)d[i][j]=min(d[i][j],d[i][k]+d[k][j]);
    return d;
}
int TreeComponentsOracle(const Matrix&a) {
    int n=static_cast<int>(a.size());vector<int> parent(n);for(int i=0;i<n;i++)parent[i]=i;
    auto root=[&parent](int v){while(parent[v]!=v)v=parent[v];return v;};
    for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(a[i][j])parent[root(i)]=root(j);
    vector<int> nodes(n),edges(n);
    for(int i=0;i<n;i++){nodes[root(i)]++;for(int j=i+1;j<n;j++)if(a[i][j])edges[root(i)]++;}
    int count=0;for(int i=0;i<n;i++)if(nodes[i]&&edges[i]==nodes[i]-1)count++;return count;
}
void TestUndirected(const Matrix&a) {
    int n=static_cast<int>(a.size());ALGraph g=MakeGraph(a);g.arcnum/=2;
    assert(TreeComponentCount(g)==TreeComponentsOracle(a));
    Matrix d=Distances(a);int out[MAXSIZE];
    for(int s=0;s<n;s++)for(int t=0;t<n;t++)if(s!=t) {
        vector<int> expected;
        if(d[s][t]<10000) for(int v=0;v<n;v++)if(d[s][v]+d[v][t]==d[s][t])expected.push_back(v);
        int count=ShortestPathVertices(g,s,t,out);assert(vector<int>(out,out+count)==expected);
    }
    DestroyGraph(g);undirectedRounds++;
}
int TermsOracle(const Matrix&a) {
    int n=static_cast<int>(a.size()),full=(1<<n)-1;vector<int> prereq(n);
    for(int v=0;v<n;v++)for(int u=0;u<n;u++)if(a[u][v])prereq[v]|=1<<u;
    vector<int> dp(1<<n,10000);dp[0]=0;
    for(int mask=0;mask<=full;mask++)if(dp[mask]<10000) {
        int available=0;for(int v=0;v<n;v++)if(!(mask&(1<<v))&&(prereq[v]&mask)==prereq[v])available|=1<<v;
        for(int sub=available;sub;sub=(sub-1)&available)dp[mask|sub]=min(dp[mask|sub],dp[mask]+1);
    }
    return dp[full]==10000?-1:dp[full];
}
void TestDirected(const Matrix&a) {
    int n=static_cast<int>(a.size());ALGraph g=MakeGraph(a);
    assert(MinimumTerms(g)==TermsOracle(a));
    static int matrix[MAXSIZE][MAXSIZE];for(int i=0;i<n;i++)for(int j=0;j<n;j++)matrix[i][j]=a[i][j];
    Matrix d=Distances(a);int out[MAXSIZE];
    for(int target=0;target<n;target++) {
        vector<int> expected;for(int u=0;u<n;u++)if(d[u][target]<10000)expected.push_back(u);
        int count=VerticesReachingTarget(matrix,n,target,out);assert(vector<int>(out,out+count)==expected);
    }
    DestroyGraph(g);directedRounds++;
}
void GraphTests() {
    for(int n=0;n<=5;n++) {
        int e=n*(n-1)/2;
        for(int mask=0;mask<(1<<e);mask++) {
            Matrix a(n,vector<int>(n));int b=0;
            for(int i=0;i<n;i++)for(int j=i+1;j<n;j++,b++)if(mask&(1<<b))a[i][j]=a[j][i]=1;
            TestUndirected(a);
        }
    }
    for(int rep=0;rep<600;rep++) {
        int n=2+pick(8);Matrix a(n,vector<int>(n));
        for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(pick(4)==0)a[i][j]=a[j][i]=1;
        TestUndirected(a);
    }
    for(int n=0;n<=3;n++)for(int mask=0;mask<(1<<(n*n));mask++) {
        Matrix a(n,vector<int>(n));for(int i=0;i<n;i++)for(int j=0;j<n;j++)a[i][j]=(mask>>(i*n+j))&1;
        TestDirected(a);
    }
    for(int rep=0;rep<900;rep++) {
        int n=1+pick(7);Matrix a(n,vector<int>(n));
        for(int i=0;i<n;i++)for(int j=0;j<n;j++)if((rep%2==0?i<j:i!=j)&&pick(4)==0)a[i][j]=1;
        TestDirected(a);
    }
    cout<<"undirected graphs: "<<undirectedRounds<<" (all <=5 vertices + 600 random); directed graphs: "<<directedRounds<<" (all <=3 vertices with loops + 900 random)\n";
}

void FixedExamples() {
    int out[MAXSIZE];
    BTNode* chain=new BTNode{1,new BTNode{2,NULL,new BTNode{3,NULL,NULL}},NULL};
    BTNode* survivor=chain->lchild->rchild;
    chain=ContractSingle(chain);assert(chain==survivor&&chain->data==3);DestroyTree(chain);
    BTNode* partial=new BTNode{1,new BTNode{2,NULL,new BTNode{4,NULL,NULL}},new BTNode{3,NULL,NULL}};
    BTNode* fourth=partial->lchild->rchild;
    partial=ContractSingle(partial);assert(partial->data==1&&partial->lchild==fourth&&partial->rchild->data==3);DestroyTree(partial);
    BTNode* badshape=new BTNode{1,new BTNode{2,NULL,NULL},new BTNode{3,new BTNode{4,NULL,NULL},NULL}};
    assert(!IsLinkedMinHeap(badshape,4));DestroyTree(badshape);
    BTNode* equal=new BTNode{2,new BTNode{2,NULL,NULL},new BTNode{2,NULL,NULL}};
    assert(IsLinkedMinHeap(equal,3));DestroyTree(equal);
    TestTree({1,2,3,-1},{-1,-1,-1,-1});
    TestTree({1,3,5,-1,-1,-1,-1},{2,4,6,-1,-1,-1,-1});
    TestTree({1,2,-1,-1},{-1,3,-1,-1});
    CSNode *four=new CSNode{4,NULL,NULL}, *five=new CSNode{5,NULL,NULL};four->nextsibling=five;
    CSNode *two=new CSNode{2,four,NULL}, *three=new CSNode{3,NULL,NULL};two->nextsibling=three;
    CSNode *one=new CSNode{1,two,NULL};assert(LeafDepthSum(one,0)==5);
    delete one;delete two;delete three;delete four;delete five;
    Matrix diamond(5,vector<int>(5));
    for(auto edge:vector<pair<int,int>>{{0,1},{0,2},{1,3},{2,3},{1,4}})diamond[edge.first][edge.second]=diamond[edge.second][edge.first]=1;
    ALGraph graph=MakeGraph(diamond);graph.arcnum/=2;
    int count=ShortestPathVertices(graph,0,3,out);assert(vector<int>(out,out+count)==vector<int>({0,1,2,3}));DestroyGraph(graph);
    Matrix blocks(6,vector<int>(6));
    for(auto edge:vector<pair<int,int>>{{0,1},{1,2},{3,4},{4,5},{5,3}})blocks[edge.first][edge.second]=blocks[edge.second][edge.first]=1;
    graph=MakeGraph(blocks);graph.arcnum/=2;assert(TreeComponentCount(graph)==1);DestroyGraph(graph);
    Matrix courses(4,vector<int>(4));courses[0][2]=courses[1][2]=courses[2][3]=1;
    graph=MakeGraph(courses);assert(MinimumTerms(graph)==3);DestroyGraph(graph);
    cout<<"explicit note examples: passed\n";
}



void ArrayTests() {
    for(int rep=0;rep<2200;rep++) {
        int n=pick(23),m=pick(19);vector<int>a(n),b(m);
        for(int &v:a) { v=pick(25)-12; }
        for(int &v:b) { v=pick(25)-12; }
        if(rep%37==0&&n>=2){a[0]=INT_MIN;a[1]=INT_MAX;}
        int low=pick(25)-12, high=pick(25)-12;if(low>high)swap(low,high);
        if(rep%43==0){low=INT_MIN;high=INT_MAX;}
        vector<int>x=a,out(100,-99),expected;
        for(int v:a)if(v<low||v>high)expected.push_back(v);
        int count=DeleteValueRange(x.data(),n,low,high);
        assert(vector<int>(x.begin(),x.begin()+count)==expected);
        vector<int>sorted=a, sortedB=b;sort(sorted.begin(),sorted.end());sort(sortedB.begin(),sortedB.end());
        x=sorted;vector<int>freq(n);count=CompressCounts(x.data(),n,freq.data());
        map<int,int>groups;for(int v:sorted)groups[v]++;
        assert(count==static_cast<int>(groups.size()));int at=0;
        for(auto [value,times]:groups){assert(x[at]==value&&freq[at]==times);at++;}
        set<int>sa(a.begin(),a.end()),sb(b.begin(),b.end());expected.clear();
        for(int v:sa)if(sb.count(v))expected.push_back(v);
        count=ArrayIntersection(sorted.data(),n,sortedB.data(),m,out.data());
        assert(vector<int>(out.begin(),out.begin()+count)==expected);
        if(n&&m) {
            long long best=LLONG_MAX;
            for(int u:a)for(int v:b){long long d=(long long)u-v;if(d<0)d=-d;best=min(best,d);}
            assert(MinAbsoluteDifference(sorted.data(),n,sortedB.data(),m)==best);
        }
        int rangeCount=0;for(int v:a)if(v>=low&&v<=high)rangeCount++;
        assert(ValueRangeCount(sorted.data(),n,low,high)==rangeCount);
        int M=pick(18);vector<int>va(n),vb(m),missing(M+1),repeated(M+1),counts(M+1);
        for(int&v:va){v=pick(M+1);counts[v]++;}for(int&v:vb)v=pick(M+1);
        int mc=-1,rc=-1;MissingAndRepeated(va.data(),n,M,missing.data(),mc,repeated.data(),rc);
        expected.clear();vector<int>expectRepeated;
        for(int v=0;v<=M;v++){if(counts[v]==0)expected.push_back(v);if(counts[v]>=2)expectRepeated.push_back(v);}
        assert(vector<int>(missing.begin(),missing.begin()+mc)==expected);
        assert(vector<int>(repeated.begin(),repeated.begin()+rc)==expectRepeated);
        x=va;expected.clear();set<int>vs(vb.begin(),vb.end());for(int v:va)if(!vs.count(v))expected.push_back(v);
        count=StableSetDifference(x.data(),n,vb.data(),m,M);assert(vector<int>(x.begin(),x.begin()+count)==expected);
        expected.clear();
        for(int i=0;i+1<n;i++) {
            long long left=0,right=0;for(int j=0;j<=i;j++)left+=a[j];for(int j=i+1;j<n;j++)right+=a[j];
            if(left==right)expected.push_back(i);
        }
        count=EqualSumCuts(a.data(),n,out.data());assert(vector<int>(out.begin(),out.begin()+count)==expected);
        expected.clear();
        for(int i=1;i+1<n;i++) {
            bool ok=true;for(int j=0;j<i;j++)if(a[j]>=a[i])ok=false;
            for(int j=i+1;j<n;j++) { if(a[j]<=a[i])ok=false; }
            if(ok)expected.push_back(i);
        }
        count=OrderedPivots(a.data(),n,out.data());assert(vector<int>(out.begin(),out.begin()+count)==expected);
        long long drop=123;bool have=MaximumDrop(a.data(),n,drop);assert(have==(n>=2));
        if(have){long long best=LLONG_MIN;for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)best=max(best,(long long)a[i]-a[j]);assert(drop==best);}
        x=a;int le=-1,gs=-1,threshold=pick(21)-10;
        ThreeWayPartition(x.data(),n,threshold,le,gs);assert(0<=le&&le<=gs&&gs<=n);
        for(int i=0;i<le;i++) { assert(x[i]<threshold); }
        for(int i=le;i<gs;i++) { assert(x[i]==threshold); }
        for(int i=gs;i<n;i++) { assert(x[i]>threshold); }
        sort(x.begin(),x.end());assert(x==sorted);
        for(int k=0;k<=n;k++) {
            x=a;KeepSmallestK(x.data(),n,k);vector<int>prefix(x.begin(),x.begin()+k);sort(prefix.begin(),prefix.end());
            assert(prefix==vector<int>(sorted.begin(),sorted.begin()+k));sort(x.begin(),x.end());assert(x==sorted);
        }
        long long target=1+pick(30);int shortest=n+1;
        for(int i=0;i<n;i++){long long sum=0;for(int j=i;j<n;j++){sum+=va[j];if(sum>=target)shortest=min(shortest,j-i+1);}}
        assert(ShortestAtLeast(va.data(),n,target)==(shortest==n+1?0:shortest));
        int expectedStart=-1,bestLength=0;
        for(int i=0;i<n;i++){int j=i;while(j+1<n&&a[j+1]>a[j])j++;if(j-i+1>bestLength){bestLength=j-i+1;expectedStart=i;}}
        int start=100;assert(LongestIncreasingRun(a.data(),n,start)==bestLength&&start==expectedStart);
        long long C=pick(20),triples=0;
        for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++)if((long long)sorted[k]-sorted[i]<=C)triples++;
        assert(TightTriples(sorted.data(),n,C)==triples);
        // Non-modifying tasks all receive a/b directly; compare against the saved derived order as a sanity check.
        vector<int>again=a;sort(again.begin(),again.end());assert(again==sorted);
    }
    cout<<"arrays A01-A15: 2200 randomized rounds, all k for selection, extreme int endpoints\n";
}

LinkList MakeList(const vector<int>& values) {
    LinkList head=new LNode{0,NULL};LNode*tail=head;
    for(int v:values){tail->next=new LNode{v,NULL};tail=tail->next;}return head;
}
vector<LNode*> ListNodes(LinkList head) {
    vector<LNode*>nodes;set<LNode*>seen;
    for(LNode*p=head->next;p;p=p->next){assert(seen.insert(p).second);nodes.push_back(p);}
    return nodes;
}
void DeleteList(LinkList head) {
    while(head){LNode*next=head->next;delete head;head=next;}
}
void ListTests() {
    for(int rep=0;rep<1600;rep++) {
        int n=pick(26),m=pick(20);vector<int>a(n),b(m);
        for(int&v:a) { v=pick(13)-6; }
        for(int&v:b) { v=pick(13)-6; }
        LinkList A=MakeList(a);vector<LNode*>nodes=ListNodes(A),expected=nodes;
        ReverseList(A);reverse(expected.begin(),expected.end());assert(ListNodes(A)==expected);DeleteList(A);
        vector<int>sorted=a, sortedB=b;sort(sorted.begin(),sorted.end());sort(sortedB.begin(),sortedB.end());
        A=MakeList(sorted);LinkList B=MakeList(sortedB);nodes=ListNodes(A);auto other=ListNodes(B);
        expected.clear();int i=0,j=0;
        while(i<n||j<m){if(j==m||(i<n&&sorted[i]<=sortedB[j]))expected.push_back(nodes[i++]);else expected.push_back(other[j++]);}
        MergeSortedLists(A,B);assert(ListNodes(A)==expected&&B->next==NULL);DeleteList(A);DeleteList(B);
        A=MakeList(sorted);B=MakeList(sortedB);nodes=ListNodes(A);other=ListNodes(B);expected.clear();set<int>bs(b.begin(),b.end());
        for(int k=0;k<n;k++)if(!bs.count(sorted[k]))expected.push_back(nodes[k]);
        SubtractSortedList(A,B);assert(ListNodes(A)==expected&&ListNodes(B)==other);DeleteList(A);DeleteList(B);
        A=MakeList(a);nodes=ListNodes(A);expected.clear();int x=pick(11)-5;
        for(int group=0;group<3;group++)for(int k=0;k<n;k++){int g=a[k]<x?0:a[k]==x?1:2;if(g==group)expected.push_back(nodes[k]);}
        StableThreeGroups(A,x);assert(ListNodes(A)==expected);DeleteList(A);
        A=MakeList(a);nodes=ListNodes(A);expected.clear();long long sum=0;for(int v:a)sum+=v;
        for(int k=0;k<n;k++)if((long long)a[k]*n<=sum)expected.push_back(nodes[k]);
        DeleteAboveOriginalMean(A);assert(ListNodes(A)==expected);DeleteList(A);
        A=MakeList(a);expected=ListNodes(A);for(int k=0;k+1<n;k+=2)swap(expected[k],expected[k+1]);
        SwapAdjacentNodes(A);assert(ListNodes(A)==expected);DeleteList(A);
        if(rep%4==0)for(int k=0;k<n/2;k++)a[n-1-k]=a[k];
        A=MakeList(a);nodes=ListNodes(A);bool palindrome=true;for(int k=0;k<n;k++)if(a[k]!=a[n-1-k])palindrome=false;
        assert(IsPalindromeRestore(A)==palindrome&&ListNodes(A)==nodes);DeleteList(A);
        int bestStart=0,bestLength=0;
        for(int k=0;k<n;k++){int end=k;while(end+1<n&&a[end+1]>a[end])end++;if(end-k+1>bestLength){bestLength=end-k+1;bestStart=k;}}
        A=MakeList(a);B=MakeList({});nodes=ListNodes(A);expected.clear();vector<LNode*>chosen;
        for(int k=0;k<n;k++){if(k>=bestStart&&k<bestStart+bestLength)chosen.push_back(nodes[k]);else expected.push_back(nodes[k]);}
        ExtractLongestIncreasingRun(A,B);assert(ListNodes(A)==expected&&ListNodes(B)==chosen);DeleteList(A);DeleteList(B);
        // Shared suffix is destroyed only once by collecting all distinct owned nodes.
        A=MakeList(a);B=MakeList(b);LinkList shared=MakeList(rep%2?vector<int>{7,8}:vector<int>{});
        auto sharedNodes=ListNodes(shared);LNode*tail=A;while(tail->next)tail=tail->next;tail->next=shared->next;
        tail=B;while(tail->next)tail=tail->next;tail->next=shared->next;
        assert(FirstSharedNode(A,B)==(sharedNodes.empty()?NULL:sharedNodes[0]));
        set<LNode*>all;for(auto p:ListNodes(A))all.insert(p);for(auto p:ListNodes(B))all.insert(p);
        for(auto p:all) { delete p; }
        delete A;delete B;delete shared;
        A=MakeList(a);nodes=ListNodes(A);AppendReversedCopy(A);auto doubled=ListNodes(A);
        assert(static_cast<int>(doubled.size())==2*n);
        for(int k=0;k<n;k++){assert(doubled[k]==nodes[k]);assert(doubled[2*n-1-k]->data==a[k]);assert(find(nodes.begin(),nodes.end(),doubled[2*n-1-k])==nodes.end());}
        DeleteList(A);
        A=MakeList(a);nodes=ListNodes(A);expected.clear();i=0;j=n-1;
        while(i<=j){expected.push_back(nodes[i++]);if(i<=j)expected.push_back(nodes[j--]);}
        ReorderEnds(A);assert(ListNodes(A)==expected);DeleteList(A);
    }
    cout<<"linked lists L01-L11: 1600 randomized rounds; exact node identity/order, cycles, restoration and shared suffix\n";
}

int BruteHeight(BTNode*p){if(!p)return 0;return 1+max(BruteHeight(p->lchild),BruteHeight(p->rchild));}
bool BruteBalanced(BTNode*p){if(!p)return true;return abs(BruteHeight(p->lchild)-BruteHeight(p->rchild))<=1&&BruteBalanced(p->lchild)&&BruteBalanced(p->rchild);}
bool PathOracle(BTNode*p,long long K,vector<int>path,long long sum,vector<int>&answer){
    if(!p) return false;
    path.push_back(p->data);sum+=p->data;
    if(!p->lchild&&!p->rchild&&sum==K){answer=path;return true;}
    return PathOracle(p->lchild,K,path,sum,answer)||PathOracle(p->rchild,K,path,sum,answer);
}
BTNode* CloneTree(BTNode*p,bool mirror){
    if(!p)return NULL;
    BTNode*l=CloneTree(p->lchild,mirror),*r=CloneTree(p->rchild,mirror);
    return new BTNode{p->data,mirror?r:l,mirror?l:r};
}
bool MirrorOracle(BTNode*a,BTNode*b){
    queue<pair<BTNode*,BTNode*>>q;q.push({a,b});
    while(!q.empty()){auto[u,v]=q.front();q.pop();if(!u&&!v)continue;if(!u||!v||u->data!=v->data)return false;
        q.push({u->lchild,v->rchild});q.push({u->rchild,v->lchild});}
    return true;
}
void InsertBST(BTNode*&root,int value){
    BTNode**link=&root;while(*link){link=value<(*link)->data?&(*link)->lchild:&(*link)->rchild;}*link=new BTNode{value,NULL,NULL};
}
void ExtraTreeTests(){
    for(int rep=0;rep<1700;rep++){
        int n=pick(23);vector<int>l(n,-1),r(n,-1),values(n);vector<pair<int,int>>slots;
        if(n)slots={{0,0},{0,1}};
        for(int i=1;i<n;i++){int k=pick(static_cast<int>(slots.size()));auto[parent,side]=slots[k];slots[k]=slots.back();slots.pop_back();(side?r[parent]:l[parent])=i;slots.push_back({i,0});slots.push_back({i,1});}
        for(int&v:values)v=pick(17)-8;
        BTNode*root=MakeTree(l,r,values,n?0:-1);int height=-3;bool balanced=TreeBalanced(root,height);
        bool expected=BruteBalanced(root);assert(balanced==expected&&height==(expected?BruteHeight(root):-1));
        int out[MAXSIZE],length=-1;vector<int>path;
        for(long long K:{-8LL,0LL,7LL,19LL}){path.clear();bool found=PathOracle(root,K,{},0,path);assert(FindSumPath(root,K,out,length)==found);assert(length==static_cast<int>(path.size()));assert(vector<int>(out,out+length)==path);}
        BTNode*mirror=CloneTree(root,true);assert(MirrorEqual(root,mirror));if(mirror)mirror->data++;
        assert(MirrorEqual(root,mirror)==MirrorOracle(root,mirror));DestroyTree(mirror);
        Matrix adjacency(n,vector<int>(n));
        for(int i=0;i<n;i++)for(int j:{l[i],r[i]})if(j>=0)adjacency[i][j]=adjacency[j][i]=1;
        Matrix distances=Distances(adjacency);int diameter=0;for(int i=0;i<n;i++)for(int j=0;j<n;j++)diameter=max(diameter,distances[i][j]);
        assert(TreeDiameter(root)==diameter);DestroyTree(root);
        set<int>keySet;int count=pick(24);for(int i=0;i<count;i++)keySet.insert(pick(80)-40);
        if(rep%31==0){keySet.insert(INT_MIN);keySet.insert(INT_MAX);}
        vector<int>keys(keySet.begin(),keySet.end()),order=keys;shuffle(order.begin(),order.end(),rng);
        root=NULL;for(int v:order)InsertBST(root,v);
        long long gap=-1;bool have=MinimumBSTGap(root,gap);assert(have==(keys.size()>=2));
        if(have){long long best=LLONG_MAX;for(int i=0;i<static_cast<int>(keys.size());i++)for(int j=i+1;j<static_cast<int>(keys.size());j++)best=min(best,(long long)keys[j]-keys[i]);assert(gap==best);}else assert(gap==0);
        for(int x:{INT_MIN,-41,-1,0,39,41,INT_MAX}){int answer=123;bool found=BSTFloor(root,x,answer);auto it=keySet.upper_bound(x);bool exist=it!=keySet.begin();assert(found==exist);if(exist){--it;assert(answer==*it);}}
        DestroyTree(root);
    }
    cout<<"additional trees T05-T10: 1700 randomized shapes/BSTs; path rollback, negative values, full int keys\n";
}
int ComponentsExcludingOracle(const Matrix&a,int removed){
    int n=static_cast<int>(a.size());Matrix b=a;
    for(int i=0;i<n;i++)b[i][removed]=b[removed][i]=0;
    Matrix d=Distances(b);vector<int>seen(n);seen[removed]=1;int count=0;
    for(int i=0;i<n;i++)if(!seen[i]){count++;for(int j=0;j<n;j++)if(d[i][j]<10000)seen[j]=1;}
    return count;
}
bool ColoringOracle(const Matrix&a){
    int n=static_cast<int>(a.size());for(int mask=0;mask<(1<<n);mask++){
        bool valid=true;for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(a[i][j]&&((mask>>i)&1)==((mask>>j)&1))valid=false;
        if(valid)return true;}
    return false;
}
void ExtraGraphTests(){
    const int INF=INT_MAX/4;static int weights[MAXSIZE][MAXSIZE];int out[MAXSIZE];
    for(int rep=0;rep<1000;rep++){
        int n=1+pick(8);Matrix a(n,vector<int>(n));
        for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(pick(4)==0)a[i][j]=a[j][i]=1;
        ALGraph g=MakeGraph(a);g.arcnum/=2;
        for(int v=0;v<n;v++)assert(ComponentsWithoutVertex(g,v)==ComponentsExcludingOracle(a,v));
        assert(IsBipartite(g)==ColoringOracle(a));DestroyGraph(g);
        int m=pick(30);int edges[30][2];Matrix dynamic(n,vector<int>(n));int redundant=0;
        for(int i=0;i<m;i++){int u=pick(n),v=pick(n);edges[i][0]=u;edges[i][1]=v;Matrix d=Distances(dynamic);if(d[u][v]<10000)redundant++;dynamic[u][v]=dynamic[v][u]=1;}
        assert(RedundantEdges(n,edges,m)==redundant);
        Matrix distance(n,vector<int>(n,INF));
        for(int i=0;i<n;i++)for(int j=0;j<n;j++){
            weights[i][j]=i==j?0:pick(4)==0?pick(13):INF;distance[i][j]=weights[i][j];}
        for(int k=0;k<n;k++)for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(distance[i][k]<INF&&distance[k][j]<INF)distance[i][j]=min(distance[i][j],distance[i][k]+distance[k][j]);
        for(int source=0;source<n;source++){DijkstraDistances(weights,n,source,out);assert(vector<int>(out,out+n)==distance[source]);}
    }
    ALGraph empty{};assert(IsBipartite(empty));int edges[1][2]={{0,0}};assert(RedundantEdges(0,edges,0)==0);
    cout<<"additional graphs G05-G08: 1000 randomized rounds; all blocked vertices/sources, brute coloring and Floyd comparison\n";
}

bool ParseBrackets(const string&s,int&at,char closing){
    while(at<static_cast<int>(s.size())){
        char c=s[at];if(c==')'||c==']'||c=='}'){if(c!=closing)return false;at++;return true;}
        at++;char expected=c=='('?')':c=='['?']':'}';if(!ParseBrackets(s,at,expected))return false;
    }
    return closing=='\0';
}
struct Expression{string text;int value;};
Expression RandomPostfix(int depth){
    if(depth==0||pick(3)==0){int x=pick(6);return {string(1,static_cast<char>('0'+x)),x};}
    Expression left=RandomPostfix(depth-1),right=RandomPostfix(depth-1);char op=string("+-*")[pick(3)];
    int value=op=='+'?left.value+right.value:op=='-'?left.value-right.value:left.value*right.value;
    return {left.text+right.text+op,value};
}
void StackHeapTests(){
    for(int rep=0;rep<2200;rep++){
        int n=pick(24);string s;for(int i=0;i<n;i++)s+=string("()[]{}")[pick(6)];int at=0;
        bool expected=ParseBrackets(s,at,'\0')&&at==n;assert(BracketsMatch(s.data(),n)==expected);
        Expression e=RandomPostfix(3);int answer=0;assert(EvaluatePostfix(e.text.data(),static_cast<int>(e.text.size()),answer)&&answer==e.value);
        vector<int>a(n);for(int&v:a)v=pick(101)-50;vector<int>sorted=a;sort(sorted.begin(),sorted.end());
        vector<int>heap=a;BuildMaxHeap(heap.data(),n);for(int i=1;i<n;i++)assert(heap[(i-1)/2]>=heap[i]);
        vector<int>x=a;HeapSort(x.data(),n);assert(x==sorted);
        for(int k=0;k<=n;k++){
            vector<int>result(k);LargestK(a.data(),n,k,result.data());
            for(int i=1;i<k;i++) { assert(result[(i-1)/2]<=result[i]); }
            sort(result.begin(),result.end());assert(result==vector<int>(sorted.end()-k,sorted.end()));}
    }
    for(string bad:{"","2+","23","+23","23?","2*"}){int answer=123;assert(!EvaluatePostfix(bad.data(),static_cast<int>(bad.size()),answer));}
    cout<<"stack/heap S01-S02 H01-H02: 2200 randomized rounds; expression trees, bracket grammar, all k\n";
}
int main(){
    FixedExamples();TreeTests();GraphTests();ArrayTests();ListTests();ExtraTreeTests();ExtraGraphTests();StackHeapTests();
    cout<<"ALL 48 extracted-card tests passed\n";
}