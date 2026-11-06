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

int EqualLengthMedian(const int A[], const int B[], int n) {
    int low1 = 0, high1 = n - 1;
    int low2 = 0, high2 = n - 1;
    while (low1 < high1) {
        int mid1 = (low1 + high1) / 2;
        int mid2 = (low2 + high2) / 2;
        if (A[mid1] == B[mid2]) return A[mid1];
        int length = high1 - low1 + 1;
        if (A[mid1] < B[mid2]) {
            low1 = (length % 2 == 0) ? mid1 + 1 : mid1;
            high2 = mid2;
        } else {
            high1 = mid1;
            low2 = (length % 2 == 0) ? mid2 + 1 : mid2;
        }
    }
    return A[low1] < B[low2] ? A[low1] : B[low2];
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

for(int n=1;n<=6;n++){
 vector<vector<int>>all;vector<int>v;
 function<void(int)>gen=[&](int low){if((int)v.size()==n){all.push_back(v);return;}for(int x=low;x<=2;x++){v.push_back(x);gen(x);v.pop_back();}};gen(-2);
 for(const auto&a:all)for(const auto&b:all){auto c=a;c.insert(c.end(),b.begin(),b.end());sort(c.begin(),c.end());assert(EqualLengthMedian(a.data(),b.data(),n)==c[n-1]);}
}
for(int z=0;z<3000;z++){int n=R(1,70);auto a=RandomValues(n),b=RandomValues(n);sort(a.begin(),a.end());sort(b.begin(),b.end());auto c=a;c.insert(c.end(),b.begin(),b.end());sort(c.begin(),c.end());assert(EqualLengthMedian(a.data(),b.data(),n)==c[n-1]);}

return 0;
}
