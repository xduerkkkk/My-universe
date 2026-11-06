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