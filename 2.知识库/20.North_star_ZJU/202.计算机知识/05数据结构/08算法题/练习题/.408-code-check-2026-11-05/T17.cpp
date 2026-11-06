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

bool CheckArrayBST(const int A[], int n, int i, int &previous) {
    if (i >= n || A[i] == -1) return true;
    if (!CheckArrayBST(A, n, 2 * i + 1, previous)) return false;
    if (A[i] <= previous) return false;
    previous = A[i];
    return CheckArrayBST(A, n, 2 * i + 2, previous);
}

bool IsArrayBST(const int A[], int n) {
    int previous = -1;
    return CheckArrayBST(A, n, 0, previous);
}

#pragma GCC diagnostic ignored "-Wmisleading-indentation"

#include <algorithm>
#include <cassert>
#include <functional>
#include <numeric>
#include <random>
#include <sstream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <iostream>
#include <io.h>
using namespace std;
mt19937 rng(4082026);
int R(int low,int high){return low+(int)(rng()%(unsigned)(high-low+1));}
vector<int> RandomValues(int n,int low=-12,int high=12){vector<int>a(n);for(int &x:a)x=R(low,high);return a;}
string Capture(function<void()> fn){
 fflush(stdout); FILE *f=tmpfile(); assert(f!=NULL);
 int old=_dup(_fileno(stdout)); assert(old!=-1);
 assert(_dup2(_fileno(f),_fileno(stdout))==0);
 fn(); fflush(stdout); rewind(f);
 string s; char b[1024]; size_t n;
 while((n=fread(b,1,sizeof b,f))>0)s.append(b,n);
 assert(_dup2(old,_fileno(stdout))==0); _close(old); fclose(f); return s;
}
LinkList MakeList(const vector<int>&a){LinkList L=new LNode{0,NULL};LNode *tail=L;for(int x:a){tail->next=new LNode{x,NULL};tail=tail->next;}return L;}
void FreeNodes(LNode *p){while(p){LNode *q=p->next;delete p;p=q;}}
vector<LNode*> Nodes(LNode *p){vector<LNode*>v;while(p){assert(v.size()<10000);v.push_back(p);p=p->next;}return v;}
vector<int> Values(LNode *p){vector<int>v;for(LNode*q:Nodes(p))v.push_back(q->data);return v;}
BTNode *RandomTree(int n){
 if(n==0)return NULL;
 int left=R(0,n-1);return new BTNode{R(-10,20),RandomTree(left),RandomTree(n-1-left)};
}
void FreeTree(BTNode*p){if(!p)return;FreeTree(p->lchild);FreeTree(p->rchild);delete p;}
pair<int,bool> HeightRef(BTNode*p){if(!p)return {0,true};auto a=HeightRef(p->lchild),b=HeightRef(p->rchild);return {max(a.first,b.first)+1,a.second&&b.second&&abs(a.first-b.first)<=1};}
void OrderRef(BTNode*p,vector<int>&out,int order){if(!p)return;if(order==0)out.push_back(p->data);OrderRef(p->lchild,out,order);if(order==1)out.push_back(p->data);OrderRef(p->rchild,out,order);if(order==2)out.push_back(p->data);}
string Printed(const vector<int>&a){ostringstream o;for(int x:a)o<<x<<' ';return o.str();}
BTNode *Insert(BTNode*p,int x){if(!p)return new BTNode{x,NULL,NULL};if(x<p->data)p->lchild=Insert(p->lchild,x);else if(x>p->data)p->rchild=Insert(p->rchild,x);return p;}
ALGraph MakeGraph(int n,const vector<vector<int>>&a){
 ALGraph G={};G.vexnum=n;
 for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(a[i][j]){G.vertices[i].firstarc=new ArcNode{j,G.vertices[i].firstarc};G.arcnum++;}
 return G;
}
void FreeGraph(ALGraph&G){for(int i=0;i<G.vexnum;i++){ArcNode*p=G.vertices[i].firstarc;while(p){ArcNode*q=p->nextarc;delete p;p=q;}G.vertices[i].firstarc=NULL;}}
int TopoRef(const vector<vector<int>>&a){
 int n=(int)a.size(),count=0;vector<int>perm(n);iota(perm.begin(),perm.end(),0);
 do{vector<int>pos(n);for(int i=0;i<n;i++)pos[perm[i]]=i;bool ok=true;for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(a[i][j]&&pos[i]>=pos[j])ok=false;if(ok)count++;if(count==2)return 0;}while(next_permutation(perm.begin(),perm.end()));
 return count==0?-1:1;
}
bool BoundsRef(const vector<int>&a,int i,long long low,long long high){if(i>=(int)a.size()||a[i]==-1)return true;return low<a[i]&&a[i]<high&&BoundsRef(a,2*i+1,low,a[i])&&BoundsRef(a,2*i+2,a[i],high);}
bool Connected(const vector<vector<int>>&a){int n=(int)a.size();if(!n)return false;vector<int>vis(n);vis[0]=1;queue<int>q;q.push(0);while(!q.empty()){int v=q.front();q.pop();for(int j=0;j<n;j++)if(a[v][j]&&!vis[j]){vis[j]=1;q.push(j);}}return count(vis.begin(),vis.end(),1)==n;}
bool EulerRef(const vector<vector<int>>&a){
 int n=(int)a.size();vector<pair<int,int>>edges;for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(a[i][j])edges.push_back({i,j});
 int all=(1<<(int)edges.size())-1;vector<vector<int>>memo(n,vector<int>(all+1,-1));
 function<bool(int,int)>walk=[&](int v,int mask){if(mask==all)return true;int &ans=memo[v][mask];if(ans!=-1)return ans==1;ans=0;for(int e=0;e<(int)edges.size();e++)if(!(mask&(1<<e))){int w=-1;if(edges[e].first==v)w=edges[e].second;if(edges[e].second==v)w=edges[e].first;if(w>=0&&walk(w,mask|(1<<e))){ans=1;return true;}}return false;};
 for(int i=0;i<n;i++)if(walk(i,0))return true;return false;
}

int main(){

for(int z=0;z<5000;z++){int n=R(0,80);vector<int>a(n,-1);for(int i=0;i<n;i++)if((i==0||a[(i-1)/2]!=-1)&&R(0,4)!=0)a[i]=R(0,30);assert(IsArrayBST(a.data(),n)==BoundsRef(a,0,LLONG_MIN,LLONG_MAX));}
for(int n=1;n<=100;n++){vector<int>a(n);int current=0;function<void(int)>fill=[&](int i){if(i>=n)return;fill(2*i+1);a[i]=current++;fill(2*i+2);};fill(0);assert(IsArrayBST(a.data(),n));}
int a[]={10,5,15,-1,-1,6,20};assert(!IsArrayBST(a,7));int b[]={0,-1,INT_MAX};assert(IsArrayBST(b,3));

return 0;
}
