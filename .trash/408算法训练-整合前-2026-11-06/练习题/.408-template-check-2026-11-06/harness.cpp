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

int main(){ FixedExamples(); TreeTests(); GraphTests();cout<<"all extracted-note code tests passed\n";}