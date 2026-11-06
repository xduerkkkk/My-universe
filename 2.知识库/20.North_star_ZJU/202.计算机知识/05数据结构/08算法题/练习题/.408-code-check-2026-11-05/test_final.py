from pathlib import Path
import re,json,subprocess,time,os,shutil,tempfile
ENV=os.environ.copy()
ENV["PATH"]=str(Path(shutil.which("g++")).parent)+";"+ENV["PATH"]
W=Path(__file__).parent
BIN=Path(tempfile.mkdtemp(prefix="kk408-tests-"))
(W/"binary-directory.txt").write_text(str(BIN),encoding="utf-8")
P=W.parent
cards=json.loads((W/'cards.json').read_text(encoding='utf-8'))
# Extract actual final Markdown, not the generator's copies.
common=(P/'算法分类训练-公共约定.md').read_text(encoding='utf-8')
header=re.findall(r'```cpp\n(.*?)\n```',common,re.S)[1]
assert 'typedef struct ALGraph' in header
codes={}
for f in P.glob('算法分类训练-0[1-6]-*.md'):
 text=f.read_text(encoding='utf-8')
 for m in re.finditer(r'^### ([ALTHSG]\d{2}) [^\n]+\n(.*?)(?=^#{2,3} |\Z)',text,re.M|re.S):
  blocks=re.findall(r'^> ```cpp\n(.*?)^> ```',m.group(2),re.M|re.S)
  if blocks:
   assert len(blocks)==1,m.group(1)
   codes[m.group(1)]='\n'.join(re.sub(r'^> ?', '',line) for line in blocks[0].splitlines())
assert set(codes)==set(cards),(set(cards)-set(codes),set(codes)-set(cards))
LIB=r'''
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
'''
T={}
T['A01']=r'''
for(int z=0;z<2000;z++){auto a=RandomValues(R(0,50));sort(a.begin(),a.end());auto b=a;b.erase(unique(b.begin(),b.end()),b.end());int n=Unique(a.data(),(int)a.size());assert(n==(int)b.size());assert(equal(b.begin(),b.end(),a.begin()));}
'''
T['A02']=r'''
for(int z=0;z<2000;z++){auto a=RandomValues(R(0,50));int x=R(-15,15);auto b=a;b.erase(remove(b.begin(),b.end(),x),b.end());int n=RemoveValue(a.data(),(int)a.size(),x);assert(n==(int)b.size());assert(equal(b.begin(),b.end(),a.begin()));}
'''
T['A12']=r'''
for(int z=0;z<4000;z++){auto a=RandomValues(R(0,50),-20,60);set<int>s(a.begin(),a.end());int ans=1;while(s.count(ans))ans++;auto before=a;assert(FirstMissingPositive(a.data(),(int)a.size())==ans);assert(a==before);}
int a[]={INT_MIN,INT_MAX,1};assert(FirstMissingPositive(a,3)==2);
'''
T['A16']=r'''
for(int z=0;z<2000;z++){auto a=RandomValues(R(0,80));sort(a.begin(),a.end());for(int x=-14;x<=14;x++){assert(LowerBound(a.data(),(int)a.size(),x)==lower_bound(a.begin(),a.end(),x)-a.begin());assert(UpperBound(a.data(),(int)a.size(),x)==upper_bound(a.begin(),a.end(),x)-a.begin());}}
int a[]={INT_MIN,INT_MIN,0,INT_MAX};assert(LowerBound(a,4,INT_MIN)==0);assert(UpperBound(a,4,INT_MAX)==4);
'''
T['A18']=r'''
for(int z=0;z<1200;z++){auto a=RandomValues(R(1,40));auto sorted=a;sort(sorted.begin(),sorted.end());for(int k=1;k<=(int)a.size();k++){auto b=a;assert(SelectK(b.data(),(int)b.size(),k)==sorted[k-1]);sort(b.begin(),b.begin()+k);assert(equal(b.begin(),b.begin()+k,sorted.begin()));b=a;SmallestK(b.data(),(int)b.size(),k);sort(b.begin(),b.begin()+k);assert(equal(b.begin(),b.begin()+k,sorted.begin()));sort(b.begin(),b.end());assert(b==sorted);}}
'''
T['A19']=r'''
for(int z=0;z<2500;z++){auto a=RandomValues(R(2,10),-100,100);int n=(int)a.size(),k=n/2;long long total=accumulate(a.begin(),a.end(),0LL),best=0;for(int mask=0;mask<(1<<n);mask++)if(__builtin_popcount((unsigned)mask)==k){long long s=0;for(int i=0;i<n;i++)if(mask&(1<<i))s+=a[i];best=max(best,llabs(total-2*s));}assert(BalancedDifference(a.data(),n)==best);}
int a[]={-100,-99,1};assert(BalancedDifference(a,3)==200);
'''
T['A20']=r'''
for(int z=0;z<2500;z++){auto a=RandomValues(R(0,40));auto before=a;vector<long long>out(a.size());SuffixMaxProduct(a.data(),(int)a.size(),out.data());for(int i=0;i<(int)a.size();i++){long long best=LLONG_MIN;for(int j=i;j<(int)a.size();j++)best=max(best,(long long)a[i]*a[j]);assert(best==out[i]);}assert(a==before);}
int a[]={INT_MIN,INT_MAX,0,-1};long long out[4];SuffixMaxProduct(a,4,out);assert(out[0]==(long long)INT_MIN*INT_MIN);
'''
T['A24']=r'''
for(int z=0;z<3000;z++){auto a=RandomValues(R(0,50));auto b=a;int p=(z%9==0)?INT_MAX:R(0,1000);if(!b.empty())rotate(b.begin(),b.begin()+p%(int)b.size(),b.end());LeftRotate(a.data(),(int)a.size(),p);assert(a==b);}
'''
T['A25']=r'''
for(int n=1;n<=6;n++){
 vector<vector<int>>all;vector<int>v;
 function<void(int)>gen=[&](int low){if((int)v.size()==n){all.push_back(v);return;}for(int x=low;x<=2;x++){v.push_back(x);gen(x);v.pop_back();}};gen(-2);
 for(const auto&a:all)for(const auto&b:all){auto c=a;c.insert(c.end(),b.begin(),b.end());sort(c.begin(),c.end());assert(EqualLengthMedian(a.data(),b.data(),n)==c[n-1]);}
}
for(int z=0;z<3000;z++){int n=R(1,70);auto a=RandomValues(n),b=RandomValues(n);sort(a.begin(),a.end());sort(b.begin(),b.end());auto c=a;c.insert(c.end(),b.begin(),b.end());sort(c.begin(),c.end());assert(EqualLengthMedian(a.data(),b.data(),n)==c[n-1]);}
'''
T['A26']=r'''
for(int z=0;z<4000;z++){auto a=RandomValues(R(0,50),-3,3);map<int,int>freq;for(int x:a)freq[x]++;int ans=-1;for(auto p:freq)if(p.second>(int)a.size()/2)ans=p.first;assert(Majority(a.data(),(int)a.size())==ans);}
'''
T['A27']=r'''
for(int z=0;z<3000;z++){auto a=RandomValues(R(1,7)),b=RandomValues(R(1,7)),c=RandomValues(R(1,7));sort(a.begin(),a.end());sort(b.begin(),b.end());sort(c.begin(),c.end());long long best=LLONG_MAX;for(int x:a)for(int y:b)for(int v:c)best=min(best,llabs((long long)x-y)+llabs((long long)y-v)+llabs((long long)v-x));assert(MinTripleDistance(a.data(),(int)a.size(),b.data(),(int)b.size(),c.data(),(int)c.size())==best);}
int a[]={INT_MIN},b[]={0},c[]={INT_MAX};assert(MinTripleDistance(a,1,b,1,c,1)==8589934590LL);
'''
T['L01']=r'''
for(int z=0;z<1000;z++){auto a=RandomValues(R(0,60));LinkList L=MakeList(a);auto nodes=Nodes(L->next);ReverseList(L);reverse(a.begin(),a.end());reverse(nodes.begin(),nodes.end());assert(Values(L->next)==a);assert(Nodes(L->next)==nodes);FreeNodes(L);}
'''
T['L02']=r'''
for(int z=0;z<1000;z++){auto a=RandomValues(R(0,35)),b=RandomValues(R(0,35));sort(a.begin(),a.end());sort(b.begin(),b.end());LinkList La=MakeList(a),Lb=MakeList(b);auto nodes=Nodes(La->next),nb=Nodes(Lb->next);nodes.insert(nodes.end(),nb.begin(),nb.end());stable_sort(nodes.begin(),nodes.end(),[](LNode*p,LNode*q){return p->data<q->data;});MergeLists(La,Lb);assert(Nodes(La->next)==nodes);assert(Lb->next==NULL);FreeNodes(La);FreeNodes(Lb);}
'''
T['L05']=r'''
for(int z=0;z<1000;z++){auto a=RandomValues(R(2,60));LinkList L=MakeList(a);auto nodes=Nodes(L->next);int split=((int)a.size()+1)/2;LNode*second=SplitHalf(L);assert(Nodes(L->next)==vector<LNode*>(nodes.begin(),nodes.begin()+split));assert(Nodes(second)==vector<LNode*>(nodes.begin()+split,nodes.end()));FreeNodes(L);FreeNodes(second);}
'''
T['L07']=r'''
for(int z=0;z<1600;z++){auto a=RandomValues(R(0,70));LinkList L=MakeList(a);auto nodes=Nodes(L->next);vector<LNode*>expected;int i=0,j=(int)nodes.size()-1;while(i<=j){expected.push_back(nodes[i++]);if(i<=j)expected.push_back(nodes[j--]);}ReorderList(L);assert(Nodes(L->next)==expected);FreeNodes(L);}
'''
T['L09']=r'''
for(int z=0;z<1200;z++){LinkList La=MakeList(RandomValues(R(0,15))),Lb=MakeList(RandomValues(R(0,15)));LNode *ta=La,*tb=Lb;while(ta->next)ta=ta->next;while(tb->next)tb=tb->next;LinkList shared=MakeList(RandomValues(R(0,15)));LNode*first=shared->next;delete shared;ta->next=first;tb->next=first;assert(FirstCommonNode(La,Lb)==first);ta->next=NULL;tb->next=NULL;FreeNodes(La);FreeNodes(Lb);FreeNodes(first);}
'''
T['L14']=r'''
for(int z=0;z<180;z++){auto a=RandomValues(R(0,25));LinkList L=MakeList(a);int k=R(-2,28);int success=-1;string out=Capture([&]{success=FindKthFromEnd(L,k);});if(k>=1&&k<=(int)a.size()){assert(success==1);assert(out==to_string(a[a.size()-k]));}else{assert(success==0);assert(out.empty());}FreeNodes(L);}
'''
T['L15']=r'''
for(int z=0;z<1600;z++){int m=R(0,30);auto a=RandomValues(R(0,70),-m,m);LinkList L=MakeList(a);vector<LNode*>expected;set<int>s;for(LNode*p:Nodes(L->next))if(s.insert(abs(p->data)).second)expected.push_back(p);RemoveAbsDuplicates(L,m);assert(Nodes(L->next)==expected);FreeNodes(L);}
'''
T['T01']=r'''
for(int z=0;z<1800;z++){BTNode*p=RandomTree(R(0,75));auto ref=HeightRef(p);assert(TreeHeight(p)==ref.first);assert(IsBalanced(p)==ref.second);FreeTree(p);}
'''
T['T05']=r'''
for(int z=0;z<1800;z++){BTNode*root=RandomTree(R(0,75));long long wpl=0,sum=0;queue<pair<BTNode*,int>>q;if(root)q.push({root,0});while(!q.empty()){auto x=q.front();q.pop();BTNode*p=x.first;int d=x.second;sum+=d;if(!p->lchild&&!p->rchild)wpl+=(long long)p->data*d;if(p->lchild)q.push({p->lchild,d+1});if(p->rchild)q.push({p->rchild,d+1});}assert(WPL(root,0)==wpl);assert(DepthSum(root,0)==sum);FreeTree(root);}
'''
T['T07']=r'''
for(int z=0;z<60;z++){BTNode*p=RandomTree(R(0,35));vector<int>a,b,c;OrderRef(p,a,0);OrderRef(p,b,1);OrderRef(p,c,2);assert(Capture([&]{PreOrder(p);})==Printed(a));assert(Capture([&]{InOrder(p);})==Printed(b));assert(Capture([&]{PostOrder(p);})==Printed(c));FreeTree(p);}
'''
T['T16']=r'''
function<ExprNode*(int)>make=[&](int leaves)->ExprNode*{if(leaves==1)return new ExprNode{(char)('a'+R(0,5)),NULL,NULL};int left=R(1,leaves-1);const string ops="+-*/";return new ExprNode{ops[R(0,3)],make(left),make(leaves-left)};};
function<string(ExprNode*,bool)>format=[&](ExprNode*p,bool isRoot){if(!p)return string();if(!p->lchild)return string(1,p->data);string s=format(p->lchild,false)+string(1,p->data)+format(p->rchild,false);return isRoot?s:"("+s+")";};
function<void(ExprNode*)>destroy=[&](ExprNode*p){if(!p)return;destroy(p->lchild);destroy(p->rchild);delete p;};
assert(Capture([&]{ExpressionToInfix(NULL);}).empty());
for(int z=0;z<120;z++){ExprNode*p=make(R(1,16));assert(Capture([&]{ExpressionToInfix(p);})==format(p,true));destroy(p);}
ExprNode a={'a',NULL,NULL},b={'b',NULL,NULL},c={'c',NULL,NULL},minus={'-',&b,&c},root={'-',&a,&minus};assert(Capture([&]{ExpressionToInfix(&root);})=="a-(b-c)");
'''
T['T17']=r'''
for(int z=0;z<5000;z++){int n=R(0,80);vector<int>a(n,-1);for(int i=0;i<n;i++)if((i==0||a[(i-1)/2]!=-1)&&R(0,4)!=0)a[i]=R(0,30);assert(IsArrayBST(a.data(),n)==BoundsRef(a,0,LLONG_MIN,LLONG_MAX));}
for(int n=1;n<=100;n++){vector<int>a(n);int current=0;function<void(int)>fill=[&](int i){if(i>=n)return;fill(2*i+1);a[i]=current++;fill(2*i+2);};fill(0);assert(IsArrayBST(a.data(),n));}
int a[]={10,5,15,-1,-1,6,20};assert(!IsArrayBST(a,7));int b[]={0,-1,INT_MAX};assert(IsArrayBST(b,3));
'''
T['T18']=r'''
for(int z=0;z<1800;z++){auto a=RandomValues(R(0,70),-100,100);BTNode*root=NULL;for(int x:a)root=Insert(root,x);int target=z%20==0?INT_MIN:(z%20==1?INT_MAX:R(-120,120));BTNode*out=ClosestBST(root,target);if(a.empty())assert(out==NULL);else{int best=a[0];for(int x:a)if(make_pair(llabs((long long)x-target),x)<make_pair(llabs((long long)best-target),best))best=x;assert(out!=NULL&&out->data==best);}FreeTree(root);}
BTNode*root=NULL;for(int x:{0,INT_MIN,INT_MAX})root=Insert(root,x);assert(ClosestBST(root,INT_MIN)->data==INT_MIN);assert(ClosestBST(root,INT_MAX)->data==INT_MAX);FreeTree(root);
'''
T['T19']=r'''
for(int z=0;z<1800;z++){auto a=RandomValues(R(0,70),-100,100);BTNode*root=NULL;for(int x:a)root=Insert(root,x);int low=R(-120,120),high=R(-120,120);set<int>s(a.begin(),a.end());vector<int>expected;for(int x:s)if(x>=low&&x<=high)expected.push_back(x);vector<int>out(a.size()+1);int n=BSTRange(root,low,high,out.data());assert(n==(int)expected.size());assert(equal(expected.begin(),expected.end(),out.begin()));FreeTree(root);}
'''
T['S04']=r'''
for(int z=0;z<1800;z++){BTNode*p=RandomTree(R(0,100));vector<int>expected;OrderRef(p,expected,1);vector<int>out(expected.size()+1);int n=IterInorder(p,out.data());assert(n==(int)expected.size());assert(equal(expected.begin(),expected.end(),out.begin()));FreeTree(p);}
'''
T['G07']=r'''
for(int n=0;n<=4;n++){
 vector<pair<int,int>>edges;for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(i!=j)edges.push_back({i,j});
 for(int mask=0;mask<(1<<(int)edges.size());mask++){vector<vector<int>>a(n,vector<int>(n));for(int e=0;e<(int)edges.size();e++)if(mask&(1<<e))a[edges[e].first][edges[e].second]=1;ALGraph G=MakeGraph(n,a);assert(UniqueTopo(G)==TopoRef(a));FreeGraph(G);}
}
for(int z=0;z<350;z++){int n=R(0,7);vector<vector<int>>a(n,vector<int>(n));for(auto&row:a)for(int&x:row)x=R(0,4)==0;ALGraph G=MakeGraph(n,a);assert(UniqueTopo(G)==TopoRef(a));FreeGraph(G);}
'''
T['G13']=r'''
for(int z=0;z<2000;z++){int n=R(0,35);vector<vector<int>>a(n,vector<int>(n));for(auto&row:a)for(int&x:row)x=R(0,3)==0;int expected=0;for(int i=0;i<n;i++){int in=0,out=0;for(int j=0;j<n;j++){out+=a[i][j];in+=a[j][i];}expected+=out>in;}ALGraph G=MakeGraph(n,a);assert(CountKVertices(G)==expected);FreeGraph(G);}
'''
T['G14']=r'''
for(int z=0;z<600;z++){int n=R(1,15);vector<vector<int>>a(n,vector<int>(n));for(auto&row:a)for(int&x:row)x=R(0,5)==0;auto reach=a;for(int i=0;i<n;i++)reach[i][i]=1;for(int k=0;k<n;k++)for(int i=0;i<n;i++)for(int j=0;j<n;j++)reach[i][j]|=reach[i][k]&&reach[k][j];ALGraph G=MakeGraph(n,a);for(int i=0;i<n;i++)for(int j=0;j<n;j++)assert(HasPath(G,i,j)==(bool)reach[i][j]);FreeGraph(G);}
'''
T['G15']=r'''
for(int n=1;n<=5;n++){
 vector<pair<int,int>>edges;for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)edges.push_back({i,j});
 for(int mask=0;mask<(1<<(int)edges.size());mask++){vector<vector<int>>a(n,vector<int>(n));for(int e=0;e<(int)edges.size();e++)if(mask&(1<<e))a[edges[e].first][edges[e].second]=a[edges[e].second][edges[e].first]=1;if(!Connected(a))continue;ALGraph G=MakeGraph(n,a);assert(HasELPath(G)==EulerRef(a));FreeGraph(G);}
}
'''
T['H01']=r'''
for(int z=0;z<2500;z++){auto a=RandomValues(R(0,150)),before=a;BuildMaxHeap(a.data(),(int)a.size());assert(is_heap(a.begin(),a.end()));sort(a.begin(),a.end());sort(before.begin(),before.end());assert(a==before);}
for(int z=0;z<1000;z++){auto a=RandomValues(R(1,70));sort(a.begin(),a.end(),greater<int>());a[0]=R(-30,30);auto before=a;HeapAdjust(a.data(),0,(int)a.size());assert(is_heap(a.begin(),a.end()));sort(a.begin(),a.end());sort(before.begin(),before.end());assert(a==before);}
'''
assert set(T)==set(codes),(set(codes)-set(T))
results=[]
for qid in sorted(codes):
 start=time.monotonic()
 # Diagnostics remain strict for note code; only compact testing helpers suppress indentation warnings.
 source=header+'\n\n'+codes[qid]+'\n\n#pragma GCC diagnostic ignored "-Wmisleading-indentation"\n'+LIB+'\nint main(){\n'+T[qid]+'\nreturn 0;\n}\n'
 cpp=W/(qid+'.cpp');exe=BIN/(qid+'.exe')
 cpp.write_text(source,encoding='utf-8')
 cmd=['g++','-std=c++17','-Wall','-Wextra','-Werror','-pedantic','-O2',str(cpp),'-o',str(exe)]
 c=subprocess.run(cmd,env=ENV,capture_output=True,encoding='utf-8',errors='replace',timeout=90)
 if c.returncode:
  print(qid,'COMPILE FAILED\n'+c.stdout+c.stderr,flush=True)
  raise SystemExit(1)
 r=subprocess.run([str(exe.resolve())],env=ENV,capture_output=True,encoding='utf-8',errors='replace',timeout=90)
 if r.returncode:
  print(qid,'TEST FAILED',r.returncode,'\n'+r.stdout+r.stderr,flush=True)
  raise SystemExit(2)
 assert r.stdout=='',(qid,r.stdout)
 elapsed=round(time.monotonic()-start,2)
 print(qid,'PASS',elapsed,'seconds',flush=True)
 results.append({'id':qid,'compiled':True,'tested':True,'elapsed_seconds':elapsed})
(W/'test-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('ALL',len(results),'FINAL NOTE CARDS COMPILED AND TESTED',flush=True)
