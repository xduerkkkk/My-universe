from pathlib import Path
import json,re,textwrap,hashlib,shutil
ROOT=Path('2.知识库/20.North_star_ZJU/202.计算机知识/05数据结构/08算法题')
if (ROOT/'练习题/.408-integrated-check-2026-11-06/published.json').exists():
    raise SystemExit('Already published; generator refuses to overwrite later work. Use validate/audit.')

BASE=ROOT/'练习题'
CHECK=BASE/'.408-integrated-check-2026-11-06'
TRASH=Path('.trash/408算法训练-整合前-2026-11-06')
NAMES={'A':'算法分类训练-01-A数组与线性表.md','L':'算法分类训练-02-L链表.md','T':'算法分类训练-03-T树与递归.md','S':'算法分类训练-04-S栈与队列.md','G':'算法分类训练-05-G图.md','H':'算法分类训练-06-H堆与排序.md'}
ENTRY='算法分类训练-00总入口.md';PUBLIC='算法分类训练-公共约定.md';RECORD='算法分类训练-整理与校验记录.md'
TEMPLATE='03算法题模板.md'
KEEP=[ROOT/TEMPLATE,*[BASE/n for n in NAMES.values()],BASE/ENTRY,BASE/PUBLIC,BASE/RECORD]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(s):return textwrap.dedent(s).strip()+'\n'
def write(p,s):
 assert '\ufffd' not in s and not re.search(r'[\x00-\x08\x0b-\x1f]',s),str(p)
 p.write_text(s,encoding='utf-8')
def safe_trash(p):
 assert p.resolve().is_relative_to(TRASH.resolve())
 assert TRASH.resolve().is_relative_to(Path('.trash').resolve())
 return p
CARDS=[]
def add(id,title,group,source,question,signal,state,steps,reason,cost,tests,code,pitfall):
 CARDS.append(dict(id=id,title=title,group=group,source=source,question=question,signal=signal,state=state,steps=steps,reason=reason,cost=cost,tests=tests,code=clean(code),pitfall=pitfall))

add('A01','稳定删除一个值域区间','A1','旧稳定删除题升级',
'给定任意整数数组A与长度n，原地删除所有值位于闭区间[low,high]的元素（low≤high），其他元素相对次序不变。返回新有效长度。要求O(n)时间、O(1)额外空间；n可为0。',
'“原地＋保序筛选”先想读写指针，不是一边删一边移动整个后缀。',
'r为下一个读取位置；A[0..w-1]是已读部分保留下来的稳定结果。w≤r，因此写入不会破坏尚未读取的数据。',
['w置0，r从0扫描至n-1。','值小于low或大于high才写入A[w++]。','返回w；后面的旧内容无须清零。'],
'每个合法元素按原顺序写入且恰写一次，被删除元素不占结果位置。',
'O(n)／O(1)。',
'[1,4,2,5,3]删[2,4] → 长度2、有效前缀[1,5]；全部删除→0；空数组→0。',
'''
int DeleteValueRange(int A[], int n, int low, int high) {
    int w = 0;
    for (int r = 0; r < n; r++)
        if (A[r] < low || A[r] > high) A[w++] = A[r];
    return w;
}
''','返回长度不是最后下标；保留条件用“或”；不要求清空失效后缀。')
add('A02','有序数组压缩并记录重复次数','A1','旧有序去重题升级',
'非递减数组A长度n，将不同值按升序原地保存在A前缀，在调用者提供的counts[]中同步保存每个值原来出现的次数。返回不同值个数，counts容量≥n。O(n)时间，除输出counts外O(1)工作空间。',
'“有序重复段＋保序压缩”是读写前缀；相等项并入上一组，而非输出新项。',
'w是已建立组数；A[w-1]是最后一组的值，counts[w-1]是其频次；读指针r仍扫描原输入。',
['遇到第一项或与末组值不同，写新组并令频次为1。','否则仅将末组频次加1。','扫描结束返回w。'],
'非递减性保证每个值连续出现；一个值只会建立一组。覆盖位置不超过r，不影响未读区。',
'O(n)／O(1)工作空间，counts输出容量O(n)。',
'[1,1,2,4,4,4] → 值[1,2,4]、次数[2,1,3]；[7,7]→[7]与[2]；空→0。',
'''
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
''','必须有序；不能把w误当频次；本题输出数组不得与A重叠。')
add('A03','两个有序数组的集合交集','A2','旧有序合并机制重设计',
'两个非递减数组A、B分别长n、m，内部可重复。将两数组公共的不同值按升序写入out[]，每值只写一次，返回个数。out与输入不重叠且容量≥min(n,m)。不得修改输入，要求O(n+m)时间、O(1)工作空间（输出另计）。',
'“两个有序序列＋匹配”同步推进；更小值在对面尚未扫描区不可能匹配。',
'i,j为两个首个未处理位置；out[0..k-1]是已确定的不同公共值。',
['A[i]小则i前进，B[j]小则j前进。','相等时若与out末值不同就写入；然后i、j均前进。','任一数组结束就返回k。'],
'丢弃较小者不会错过匹配；相等值有一对即可确认为集合公共值，输出去重保证每值只一次。',
'O(n+m)／O(1)工作空间。',
'A=[1,1,2,4]，B=[1,1,1,3,4] → [1,4]；任一空→空；不能输出两个1。',
'''
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
''','集合交集不是多重集交集；输入有重复也只输出一个。')
add('A04','两个有序数组的最小绝对差','A2','保留旧A06好题',
'两个非空非递减整数数组A、B，长度n、m。任取A与B各一项，求最小绝对差，不修改输入。要求O(n+m)时间、O(1)空间，差用long long表示。',
'“有序＋跨序列最优配对”先比较当前值；只推进较小的一方才可能缩小当前差。',
'i,j沿两数组只前进；best为已经检查过的配对的最小差。',
['用首对初始化best。','检查当前差；若为0可直接返回。','A[i]<B[j]时i前进，否则j前进，直至一方耗尽。'],
'当A[i]≤B[j]时，用同一个A[i]配B的更后元素不会更好；故可丢弃A[i]。对另一侧对称。',
'O(n+m)／O(1)。',
'A=[1,5,10]、B=[3,8]→2；[-5]与[2]→7；相等值→0；INT_MIN与INT_MAX的差须提升类型。',
'''
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
''','两数组须非空；先转long long再减，不能int减完再转换；不用排序，因为输入已排序。')
add('A05','有序数组中一个值域内有多少项','A4','旧二分边界题应用化',
'非递减数组A长度n，允许重复。对给定low≤high，求值属于闭区间[low,high]的元素个数，不修改输入。要求O(log(n+1))时间、O(1)空间；n可为0。',
'“有序＋统计连续值域＋对数时间”转成两个边界，不逐项计数。',
'FirstAtLeast返回首个≥x的位置；FirstGreater返回首个>x的位置；不存在返回n。二分未决区间统一用闭区间[low,high]。',
['分别二分首个≥low的位置L、首个>high的位置R。','每次命中条件记录mid为候选，继续向左找。','返回R-L。'],
'有效元素恰好落在下标半开区间[L,R)，因此差即数量。',
'O(log(n+1))／O(1)。',
'[1,2,2,4,7]查询[2,4]→3；[3,3]→0；[1,7]→5；空→0。',
'''
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
''','不要用high+1代替严格大于边界，high可能为INT_MAX；n是合法的“未找到”位置。')
add('A06','有限值域内的缺失值与重复值','A3','计数数组基础重设计',
'数组A长n，各值保证属于0..M，M≥0。将0..M中未出现的值递增写入missing[]，出现至少两次的不同值递增写入repeated[]；通过引用返回两种数量。两输出容量均≥M+1且不重叠。不得修改输入，O(n+M+1)时间，可用O(M+1)空间。',
'“小而明确的值域＋出现次数”用值作下标；不需要哈希或排序。',
'freq[v]是值v出现次数；missingCount/repeatedCount是两个输出长度。',
['申请M+1个零初始化频次槽。','扫描输入累加。','从0到M扫描，0次记缺失，至少2次记重复。','释放频次表。'],
'每个值的槽恰保存全部出现次数；按值扫描保证结果升序且每值只输出一次。',
'O(n+M+1)／O(M+1)，两个输出另计。',
'A=[0,2,2,4]、M=4 → 缺失[1,3]、重复[2]；空数组M=0→缺失[0]。',
'''
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
''','值域不是数组长度；有一个值出现3次也只输出一次；申请范围含M。')
add('A07','两个无序数组的集合差','A3','自编：标记与原地稳定筛选组合',
'A、B为无序数组，长度n、m，值均在0..M。原地稳定删除A中所有在B出现过的值，保留A中其他项及其重复次数，返回新长度。不得修改B；O(n+m+M+1)时间、O(M+1)空间。',
'“无序成员判断＋保序删除”不是有序归并，是值域标记A3＋读写前缀A1。',
'seen[v]只表示v是否出现在B；w保存A的有效结果长度。',
['将B的值标为已出现。','扫描A，未在B标记的值稳定写回前缀。','释放标记，返回w。'],
'保留条件只依赖固定集合B，扫描A不会改变它；写回顺序与原A一致。',
'O(n+m+M+1)／O(M+1)。',
'A=[3,1,3,2,4]、B=[1,2,2]、M=4 → [3,3,4]；B为空→A不变。',
'''
int StableSetDifference(int A[], int n, const int B[], int m, int M) {
    int *seen = new int[M + 1]();
    for (int j = 0; j < m; j++) seen[B[j]] = 1;
    int w = 0;
    for (int r = 0; r < n; r++)
        if (seen[A[r]] == 0) A[w++] = A[r];
    delete[] seen;
    return w;
}
''','这里不是“结果去重”；A里合法重复项必须都保留；不能把seen改成扫描A的已出现表。')
add('A08','左右两段和相等的切分位置','A5','自编：固定总量＋前缀累计',
'任意整数数组A长n，找出所有切分下标i，使左段A[0..i]与右段A[i+1..n-1]均非空且和相等。将i递增写入out[]，容量≥n，返回个数。不得修改A；O(n)时间、O(1)工作空间，和用long long。',
'“所有切分点＋左右总和”先求总量，再用当前前缀补出右侧；负数不妨碍这种恒等式。',
'left为截至i的前缀和；右侧为total-left；不必建完整前缀数组。',
['第一遍求total。','第二遍只枚举i<n-1，先累加A[i]。','left==total-left时写入i。'],
'每个合法切分恰枚举一次，等式精确对应两段和。',
'O(n)／O(1)工作空间。',
'[1,-1,0,0]→[1,2]；[2,2]→[0]；n<2→空；全0长4→[0,1,2]。',
'''
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
''','不能包含i=n-1的空右段；前缀求和可处理负数，不要误套按和收缩窗口。')
add('A09','左侧都小而右侧都大的内部位置','A5','保留旧A23好题并明确严格性',
'任意整数数组A长n，输出所有内部下标i（1≤i≤n-2），使其左边每项严格小于A[i]、右边每项严格大于A[i]。结果按下标升序写入out[]，容量≥n；不改A，O(n)时间，可用O(n)空间。',
'“每个位置都要比较整侧”预处理后缀最小值，扫描维护左侧最大值，不能逐点双重扫描。',
'rightMin[i]为A[i..n-1]最小值；处理i前leftMax为A[0..i-1]最大值。',
['n<3直接返回0；从右构造rightMin。','leftMax初始A[0]，枚举内部i。','用leftMax<A[i]且A[i]<rightMin[i+1]判断，再把A[i]并入leftMax。'],
'整侧“全部小／大”分别等价于左侧最大值小、右侧最小值大；两侧均排除当前值。',
'O(n)／O(n)。',
'[1,2,3,4]→[1,2]；[1,2,2,3]→空（严格）；[3,1,4,5]→[2]。',
'''
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
''','判断前不能把自己放进leftMax；右边查i+1不是i；重复相等不合格。')
add('A10','先出现的大值与后出现的小值的最大落差','A5','自编：先查询历史最优再更新',
'任意整数数组A长n，求max{A[i]-A[j] | 0≤i<j<n}。必须选一对，结果可以为负；n<2返回false，否则通过answer返回long long结果并返回true。不改A，O(n)时间、O(1)空间。',
'“i<j＋可拆的二元表达式”固定j，只需要此前最大的A[i]。',
'previousMax只含下标<j的值；answer是已处理合法配对的最大落差。',
['n<2返回false；用A[0]-A[1]初始化答案。','j从1扫描，先用previousMax-A[j]更新答案。','之后才将A[j]并入previousMax。'],
'对固定j最好的i就是前缀最大值；遍历全部j覆盖全体合法配对。',
'O(n)／O(1)。',
'[2,5,1,4]→4；[1,2,3]→-1，不是0；[7,7]→0；单点→false。',
'''
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
''','答案不能初始为0；先更新历史再算会允许i=j；类型提升要发生在相减前。')
add('A11','按阈值原地分成三段','A6','保留旧荷兰国旗机制并统一答案',
'给定任意整数数组A长n及阈值x，原地分成“小于x、等于x、大于x”三段，段内无需有序或稳定。通过lessEnd和greaterStart返回中段的半开区间[lessEnd,greaterStart)，可以为空。O(n)时间、O(1)空间，不可调用排序。',
'“只需分区不需排序”维护已确定区域与未处理区；三类用三个边界。',
'[0,less)小于x，[less,i)等于x，[i,greater]未知，(greater,n)大于x。',
['less=i=0，greater=n-1。','小于：与less交换后less和i都加1。','等于：只让i加1。','大于：与greater交换并让greater减1，i不动。','结束中段为[less,greater+1)。'],
'每步把一个未知元素归类，并保持四段不变量；未知区长度严格减小。',
'O(n)／O(1)。',
'[3,1,2,2,5]阈值2 → 三段值集合[1]、[2,2]、[3,5]，中段[1,3)；全大于→[0,0)；空→[0,0)。',
'''
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
''','换回未知区的右端元素还没分类，因此大于分支不能i++；分区不承诺稳定。')
add('A12','原地保留最小的k个数','A6','保留快速选择基础，非新题预测',
'任意整数数组A长n，0≤k≤n。重排后使前k个位置恰为最小的k项（重复按项计数），内部不要求有序。不申请辅助数组。不要求最坏线性，说明时间上下界；k=0或n时可不操作。',
'“只要前k项属于最小集合，不要求排序”用划分选择，只处理包含第k小位置的一侧。',
'Partition把一个枢轴放到最终位置p；目标下标为k-1；闭区间[low,high]包含尚未定位的目标。',
['k=0或n直接返回。','在当前区间做挖坑划分。','p等于k-1则完成；p偏右只缩左侧，否则只缩右侧。'],
'枢轴左侧均不大于它、右侧均不小于它；排除不含目标的一侧不会影响最小k项的归属。',
'互异值的随机排列等通常模型下平均O(n)；本固定首项枢轴实现不保证任意输入的期望线性，最坏O(n²)，额外空间O(1)。',
'[5,1,4,1,3]、k=3 → 前3项的多重集[1,1,3]，次序不限；k=0/n；全相等仍须终止。',
'''
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
''','第k小对应k-1；不对两侧都递归，否则变成快排；固定首枢轴在有序数组上可能退化。')
add('A13','非负数组最短达标连续段','A7','保留一题基础窗口，压缩旧窗口题量',
'数组A各项非负，target>0。返回和至少为target的最短非空连续段长度，不存在返回0；不改A，O(n)时间、O(1)空间。累计和用long long。',
'“连续段＋非负＋最短达标”允许同向窗口：右端增加不会减小和，左端移出不会增大和。',
'sum始终等于当前[left,right]的和；best为已找到最短长度，n+1表示尚未找到。',
['每次右端加入一项。','只要sum仍达标，先更新长度，再移出左端；必须while收缩。','最后没有合法长度则返回0。'],
'对每个右端，把可行起点推进到极限，过程中记录最短候选；left只向右，总次数≤n。',
'O(n)／O(1)。',
'[0,2,0,3]、target=3→1；[1,1]、target=3→0；空→0；含负数不在本题契约内。',
'''
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
''','target必须>0；有负数时不能照搬；先记长度再删左端；不能只if收缩一次。')
add('A14','最长连续严格递增段','A5','自编：连续段状态重置基础',
'任意整数数组A，求最长的连续严格递增段。通过start返回起点，函数返回长度；并列取最早起点；空数组返回0且start=-1。不改A，O(n)时间、O(1)空间。',
'“连续段＋相邻关系”用一段当前状态，不是最长递增子序列，也不必排序。',
'currentStart是当前严格递增段的起点；bestLength和start为已知最早最优段。',
['空数组单独处理；其他以首项初始化。','遇A[i]≤A[i-1]时将currentStart重置为i。','仅当新长度严格超过best时更新，以保留最早并列解。'],
'任何连续严格递增段都包含在一个极大递增段中；扫描恰在断点重置，并检查所有段长度。',
'O(n)／O(1)。',
'[1,2,0,1,2]→start=2、长度3；[1,2,0,1]→start=0、长度2；[2,2]→0和1；空→-1和0。',
'''
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
''','连续段不能跳过元素；相等会断开；并列更新要用>而非≥。')
add('L01','带头结点单链表原地逆置','L1','保留旧逆置积木并统一带头结点',
'带头结点L的无环单链表，原地逆置所有数据结点，头结点地址不变。不得申请或释放结点，O(n)时间、O(1)空间。L本身非NULL，空表L->next==NULL。',
'“改变next方向”先保存后继，再改边，再推进；头结点不参加逆置。',
'pre是已逆置前缀的新首，p是未处理首；next暂存原后继。',
['pre=NULL，p=L->next。','保存next=p->next，令p->next=pre。','pre=p，p=next；结束令L->next=pre。'],
'每轮将未处理前缀的一个结点移到已逆置链头，结点不丢失、不重复且最终以NULL结尾。',
'O(n)／O(1)。',
'空表不变；[1]不变；[1,2,3]→[3,2,1]，全部数据结点地址仍为原地址。',
'''
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
''','必须先存next；返回后尾next为NULL；不能把L一起逆进去。')
add('L02','复用结点稳定归并两个有序链表','L2','保留旧归并好题，明确所有权',
'两条非递减无环带头链表A、B没有共享结点。复用全部数据结点，稳定归并到A；值相等先取A原结点，两个输入各自的相对次序保持。B最终为空，两个头结点均保留。不申请或释放结点；O(n+m)时间、O(1)空间。',
'“有序两链＋重接”比较未处理首，尾插较小者。',
'p,q是两条未处理链的首，tail是结果尾；头A只作哨兵。',
['暂存两表首，清空两个头的next，tail=A。','比较p,q，较小者接到tail并推进该链，等值先A。','tail推进；最后把未耗尽的链整体接上。'],
'每次选未处理的最小值；等值优先顺序保证稳定；所有数据结点恰使用一次。',
'O(n+m)／O(1)。',
'A=[1,3,3]、B=[2,3]→A=[1,2,3,3,3]，B为空；相等项A原结点在B前；任一空。',
'''
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
''','输入不能共享结点或头；B的旧数据现归A所有，不可按原B再次释放；相等取左侧。')
add('L03','有序链表减去另一表中的值','L2','自编：有序推进＋删除所有权',
'A、B是两条非递减无环带头链表，无共享结点，内部可重复。从A中删除并释放所有值在B中出现的结点，保留其余项及重复次数，B结构和值不变。结点由new创建；O(n+m)时间、O(1)空间。',
'“有序成员匹配＋删A不动B”是同步推进与前驱删除组合，不是无序每项都重扫B。',
'pre为A中已保留尾，p为待判A结点，q为B首个可能≥p值的位置。',
['对每个p，先将q推进到不小于p->data。','q等值则A结点应删：pre绕过p，delete，p回到pre->next。','不匹配则保留，pre=p，p前进。','等值时不必推进q，以便匹配A中的重复项。'],
'B有序且A处理值不减，q丢弃的小值不可能匹配后续A；前驱始终指向保留链尾。',
'O(n+m)／O(1)。',
'A=[1,2,2,3,5]，B=[2,4]→A=[1,3,5]，B不变；B为空→A不变；全部删后A空。',
'''
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
''','删除后pre不前进；B数据结点不能释放；q相等后不推进才能一次删掉A的同值重复段。')
add('L04','按阈值稳定分成三组再连接','L2','旧稳定分组机制升级',
'带头单链表L按结点值与x的关系，稳定重排为小于x、等于x、大于x三段。复用全部数据结点，L地址不变，不申请或释放数据结点；O(n)时间、O(1)空间。',
'“链表稳定分流”用每组头尾指针尾插，不照搬数组交换。',
'head[3]/tail[3]分别维护三组数据链首尾；p为未处理首，每次摘点先断旧边。',
['三组首尾初始化NULL。','先保存p后继，再令p->next=NULL，根据值选择一组尾插。','按组0、1、2串接，跳过空组，最后令结果尾next=NULL。'],
'每个结点恰进入一组；尾插保持组内原序，拼接只改变组间顺序。',
'O(n)／O(1)，3组指针数量固定。',
'[3,1,2,4,2,0]、x=2→[1,0,2,2,3,4]；空、某组为空、全部等值；地址均保留。',
'''
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
''','先存后继；摘点后断开旧链；不能用头插，否则组内逆序；头指针不是数据结点。')
add('L05','删除所有大于原表平均值的结点','L3','保留旧L13好题',
'带头无环单链表L，删除并释放所有数据值严格大于原表平均值的数据结点。空表不变，保留相等者及相对顺序。结点由new创建；和及乘积可用long long表示；O(n)时间、O(1)空间。',
'“基于原全体统计再删除”先统计后修改，不能删除中不断重算平均数。',
'sum,count固定描述原表；pre为保留链尾，p为当前待判结点。',
['第一遍求原表sum和count。','第二遍比较1LL*p->data*count>sum，避免浮点。','删除时pre不前进，保留时pre=p。'],
'count>0时交叉相乘与比较平均数等价；固定sum,count保证用原表而非剩余表做判断。',
'O(n)／O(1)。',
'[1,2,6]均值3→[1,2]；[-3,-1]→[-3]；全相等全保留；空表不作除法。',
'''
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
''','严格大于才删；空表不除0；删除后不能读取旧p；sum,count不能随删除改变。')
add('L06','相邻数据结点两两交换','L1','自编：局部重接，不交换数据域',
'带头无环单链表L，将第1与2、3与4……个数据结点两两交换，奇数个时最后一项不变。只能修改next，不能交换data；无结点增删；O(n)时间、O(1)空间。',
'“交换结点不是交换值”画出pre→a→b→next，明确修改后的三个连接。',
'pre为待换这一对前驱；a,b为这一对，交换后a变为对尾，也是下一对前驱。',
['剩余至少两个结点才进入循环。','a连到b后继，b连到a，pre连到b。','pre=a，处理下一对。'],
'每次只重接一对及两侧接口；对内逆序、对间顺序不变，未处理链可继续访问。',
'O(n)／O(1)。',
'[1,2,3,4,5]→[2,1,4,3,5]；空、单点不变；数据值重复也应按地址交换。',
'''
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
''','不能通过交换data蒙混；交换后pre是a不是b；条件要保证b存在。')
add('L07','判断链表回文并恢复原链','L4','保留旧L06好题，辅助函数完整展开',
'带头无环单链表L，判断数据序列是否回文。允许临时改next，但返回前必须恢复全部原连接；不增删结点。O(n)时间、O(1)空间；空表与单点为真。',
'“前后对应＋单链无法逆向走＋要求恢复”拆成找中点、逆置后半、比较、恢复。',
'slow定位前半尾，奇数时包含中点；second是逆置后的后半首；ok记录比较而不提前返回。',
['快指针从首数据结点出发，每次走两步，定位slow。','逆置slow之后的后半链并接回。','从表首与second同时比较，后半耗尽即够。','无论是否相等，都再次逆置后半并接回，再返回ok。'],
'前半与后半逆序逐项相等正是回文；中间项无需配对；两次逆置恢复相同结点连接。',
'O(n)／O(1)。',
'[1,2,1]真；[1,2,2,1]真；[1,2,3]假且原链必须完整；空真。',
'''
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
''','比较失败不能立即return；奇数中点不参与后半；不要忘slow->next接回恢复结果。')
add('L08','摘出最长连续递增子链','L4','自编：扫描统计＋一次摘链组合',
'带头无环单链表L，将最长连续严格递增的数据子链完整摘出，接到调用者提供的空带头链表R（R!=L）中，其余结点在L中保持原序。并列取原来最早的一段。空L时R仍空。两表不共享结点，不申请、不释放、不改data；O(n)时间、O(1)空间。',
'“连续段定位＋物理摘链”先只读找最优段的前驱和尾，再一次性改边；不在扫描时不断拆链。',
'currentPre/currentLength描述当前递增段；bestPre/bestTail保存最早最优段边界。',
['空表返回；用首项建立长度1的候选。','沿原链扫描，下降或相等就开启新段，更新当前前驱。','仅长度严格更大时保存bestPre与bestTail。','R->next指向bestPre->next；原前驱绕过该段；段尾next置NULL。'],
'相邻关系唯一确定所有极大递增段；最长段必为其中之一。扫描后一次摘出，不影响其他结点相对顺序。',
'O(n)／O(1)。',
'[1,2,0,1,2,-1]→R=[0,1,2]、L=[1,2,-1]；[1,2,0,1]并列取前段；全递增→L空；全相等→摘首项。',
'''
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
''','R必须原本为空；长度1并列不能更新；要保存前驱而不是只有段首；摘走整表时头L仍保留。')
add('L09','按地址找两个链表的共同后缀首结点','L4','保留旧L09，改为直观长度对齐',
'两条无环带头链表A、B可能共享部分数据结点，但头结点不同。按地址找第一个公共数据结点，无交点返回NULL；不修改也不释放任何结点。O(n+m)时间、O(1)空间。',
'“无环共享尾＋地址相等”先消除长度差，再同步走，不是找值相同。',
'n,m是数据结点数；p,q在对齐后到各自末尾的剩余长度相同。',
['分别统计两链长度。','长链先走长度差步。','再同步走到p==q；若不相交最后二者同时为NULL。'],
'共享结点之后next相同，所以共享部分必为后缀；长度对齐使到共同首点的距离相等。',
'O(n+m)／O(1)。',
'两链数据值相同但结点独立→NULL；A前缀长2、B前缀长1共享尾→返回该尾首地址；空链。',
'''
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
''','必须比较指针不是data；不能按两份独立链表释放共享尾；本题不处理环。')
add('L10','在原链后接上逆序副本','L2','旧生成对称链表思路重设计',
'带头链表L含n个数据结点，将序列a1,…,an扩展为a1,…,an,an,…,a1。原数据结点保留原序且地址不变，允许恰好新建n个数据结点，不新建头结点，假定new成功。O(n)时间，除新增输出结点外O(1)工作空间；空表不变。',
'“保留原链＋追加逆序副本”原结点只读，副本用头插自动逆序，最后拼接。',
'copyHead是已复制前缀的逆序链首；tail记录最后一个原结点；扫描阶段不能提前把副本接回原链。',
['扫描原数据结点，每读一项新建副本并头插到copyHead。','同时记录原链尾tail。','原链扫描结束后令tail->next=copyHead。'],
'头插使副本顺序为an,…,a1，原链顺序未改变；最后拼接即所需序列。',
'O(n)时间；新增输出结点O(n)，除此工作空间O(1)。不能把总新增内存说成O(1)。',
'[1,2,3]→[1,2,3,3,2,1]；[7]→[7,7]；空不变；前n个结点地址保持。',
'''
void AppendReversedCopy(LinkList L) {
    LNode *copyHead = NULL, *tail = L;
    for (LNode *p = L->next; p != NULL; p = p->next) {
        LNode *copy = new LNode{p->data, copyHead};
        copyHead = copy;
        tail = p;
    }
    tail->next = copyHead;
}
''','只允许副本新分配；扫描结束前不能接入副本，否则可能继续扫描新结点而无限复制。')
# Preserve the eight reviewed pilot tasks, including their detailed derivations.
for filename,prefix,groups,signals in [
 ('408新题训练-01树与递归.md','T',['T3','T2','T5','T1'],[
  '删除/收缩会改变子树根：选T3“返回新根”，父结点必须接回。',
  '深度由祖先决定：选T2向下传参；孩子兄弟表示先重解释指针语义。',
  '完整性是跨父结点的位置限制：选T5层序空位；值约束另逐边检查。',
  '每个候选都依赖左右规模：选T1后序汇总，再用总量补外侧。']),
 ('408新题训练-02图与遍历.md','G',['G1','G1','G3','G2'],[
  '先找到一个分量再判断它：选G1全图遍历与分量汇总。',
  '所有起点到同一终点：选G1反向可达；矩阵沿列读，无须重复跑n次。',
  '先修依赖且可并行：选G3拓扑消除依赖，并冻结每轮队列末尾。',
  '无权最短路的所有相关顶点：选G2距离标号，两端距离合成筛选条件。'])]:
 text=(BASE/filename).read_text(encoding='utf-8')
 parts=re.split(r'(?=^### N[TG]\d+ )',text,flags=re.M)[1:]
 for idx,section in enumerate(parts,1):
  section=re.split(r'^## ',section,maxsplit=1,flags=re.M)[0].strip()
  match=re.match(r'### N[TG]\d+ (.+)',section)
  title=match.group(1)
  section=re.sub(r'^### N[TG]\d+ ',f'### {prefix}{idx:02d} ',section,count=1)
  source=re.search(r'^\*\*来源与定位\*\*：(.*)',section,re.M).group(1)
  if idx in ([1,3] if prefix=='T' else [1,3]):
   source=('旧T09重写' if prefix=='T' and idx==1 else '旧T15重写' if prefix=='T' else '旧G01升级' if idx==1 else '旧G06重写')+'；保留第一批已评审解析，历史原文在trash归档。'
  else: source='保留第一批自编任务；不标真题年份或出题概率。'
  section=re.sub(r'^\*\*来源与定位\*\*：.*',f'**来源与定位**：{source}',section,flags=re.M)
  needle='> [!faq]- 分析与408风格参考解答｜尝试后展开'
  assert needle in section
  section=section.replace(needle,needle+'\n> **考场识别 → '+groups[idx-1]+'**：'+signals[idx-1]+'\n>',1)
  normal='\n'.join(l[2:] if l.startswith('> ') else '' if l=='>' else l for l in section.splitlines())
  code=re.findall(r'```cpp\n(.*?)\n```',normal,re.S);assert len(code)==1
  CARDS.append(dict(id=f'{prefix}{idx:02d}',title=title,group=groups[idx-1],source=source,raw=section+'\n',code=code[0]+'\n',signal=signals[idx-1]))

add('T05','一次后序判断树高与平衡性','T1','保留旧T01后序代表题',
'二叉链表存储，判断每个结点左右子树高度差是否≤1。空树高0、叶高1。若平衡，通过height输出真实树高并返回true；否则height=-1并返回false。O(n)时间、O(h)栈空间，不得对每个结点重扫子树求高。',
'“当前结点需要两个孩子的完整结果”选后序；返回值可兼带合法/失败状态。',
'正常返回非负树高；-1表示已发现不平衡，这与合法高度不冲突。',
['空返回0。','求左高，失败即返回-1；右侧同理。','高差大于1则失败，否则返回较大高度+1。','入口把返回值交给height，检查是否非-1。'],
'归纳地，两个孩子返回准确高度或失败；本层检查恰好补上当前结点条件。',
'O(n)／O(h)，退化树h=n；不是总为O(log n)。',
'空→true,0；根加两叶→true,2；3结点单链→false,-1。',
'''
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
''','每层调用另一个求高函数最坏O(n²)；失败高度-1不能继续作为正常数值参加运算。')
add('T06','寻找路径和等于K的一条根叶路径','T2','旧根叶路径模板升级为约束搜索',
'二叉链表结点值可正可负。寻找一条从根到叶、结点值和为K的路径，将值序列写入容量≥结点数的out[]，通过length返回长度；多条时先左子树，找一条即可。成功返回true，失败返回false且length=0；空树失败。不改树，O(n)时间、O(h)递归空间。',
'“路径依赖祖先状态”向下传sum；“失败要改试兄弟”将路径长度回退。',
'sum是进入当前点之前的祖先和；out[0..length-1]是当前递归路径，length引用共享，需要在失败离开时减1。',
['空指针返回false，不压入路径。','当前值压入out，更新sum。','只有叶且sum==K才成功；否则先左后右递归。','若两边均失败，length--回退，再返回false；成功时保留整条路径。'],
'进入/失败退出维护当前祖先路径不变量；叶条件避免把内部前缀误当根叶路径。',
'O(n)／O(h)栈；out为调用者输出缓冲区，容量O(n)。',
'根1左叶2右叶3，K=4→[1,3]；K=1失败；根5左叶-2，K=3可成功，不能因5>K剪枝。',
'''
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
''','有负数不能按sum>K剪枝；sum按值传自动回退，但引用length须手动回退；必须到叶。')
add('T07','两棵树是否互为镜像','T6','保留旧双树同步代表题',
'两棵二叉树A、B采用二叉链表存储。判断结构与对应结点值是否互为镜像，不改树。两空树为真；要求线性于访问到的结点对数。',
'“两棵树同时比较”参数必须带两个指针，镜像配对为左对右、右对左。',
'函数返回“以a、b为根的两棵子树是否镜像”；空指针情况先完整分类。',
['两者都空返回真；恰一个空返回假。','值不同返回假。','递归比较a左与b右、a右与b左，两者都真才真。'],
'镜像的递归定义恰好由根值相同与交叉子树镜像组成。',
'最坏O(n+m)时间的上界；按同时访问的结点对计为O(访问对数)；空间O(min(hA,hB)+1)，也可保守写O(hA+hB)。',
'根1左2与根1右2→真；同形但左右值不同→按交叉关系判；空与非空→假。',
'''
bool MirrorEqual(BTNode *a, BTNode *b) {
    if (a == NULL && b == NULL) return true;
    if (a == NULL || b == NULL) return false;
    return a->data == b->data &&
           MirrorEqual(a->lchild, b->rchild) &&
           MirrorEqual(a->rchild, b->lchild);
}
''','必须恰一空判假；同树相等用左左/右右，镜像用左右/右左；不能只比较遍历值序列。')
add('T08','BST相邻键值的最小差','T4','自编：中序历史状态应用',
'严格BST采用二叉链表存储，键互异，允许int全范围。不改树，求任意两个不同结点键值的最小绝对差，通过long long gap输出；结点少于2返回false，此时gap=0。要求O(n)时间、O(h)递归空间，不保存中序数组。',
'“BST＋相邻有序值关系”中序变成递增流，只需上一个访问值。',
'hasPrevious表示是否已有前驱，previous记录其值；hasPair表示gap是否已初始化。不能用INT_MIN哨兵冒充未访问。',
['中序递归左侧。','有前驱时计算1LL*当前值-previous，并建立或更新gap。','将当前值存为previous，标记已有前驱，再处理右侧。'],
'有序序列中非相邻两项的差不小于中间某个相邻差，因此最小差必出现在相邻项之间。',
'O(n)／O(h)，不申请O(n)数组。',
'BST键[1,4,6,10]→2；单点false,0；INT_MIN与INT_MAX两个键→4294967295。',
'''
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
''','previous必须跨递归共享；INT_MIN可能是真实键；先提升类型再减；普通无序二叉树不成立。')
add('T09','树上任意两点的最远边数','T1','自编：局部候选与全局最优分离',
'二叉链表存储，求树上任意两结点之间简单路径的最大边数；空树、单点返回0。不改树，O(n)时间、O(h)空间。无需输出路径。',
'“最优路径可能不经过根”后序返回向下高度，并在每个点合并左右候选更新全局答案。',
'返回值为以结点数计的子树高度，空高0；穿过当前点的最长路径边数为leftHeight+rightHeight；best为全局最优，不是要返回给父亲的高度。',
['空树辅助函数返回0。','后序求左右高度。','用左右高度和更新best。','只向父亲返回max(左右高度)+1。'],
'任意简单路径有唯一最高结点，路径在其两侧各走一条向下链；枚举每个结点作为最高点即可覆盖最优路径。',
'O(n)／O(h)。',
'单点0；3点单链2；根有左右叶→2；最长路完全在某子树中也能被best记录。',
'''
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
''','向上返回的是一条向下链高度，不能返回左右高度之和；不只在根处算一次；边数和结点数要对应。')
add('T10','BST中不大于x的最大键','T4','自编：利用有序性剪去整侧子树',
'严格BST采用二叉链表存储。找出不大于x的最大键，通过answer输出并返回true；不存在返回false，此时不规定answer。不改树，要求O(h)时间、O(1)额外空间。空树可输入。',
'“BST＋一个有序边界”不必全树中序；每步保留候选后只选一侧。',
'found表示是否已有合法候选；answer是当前路径上找到的最大合法键；p是尚可能改进它的子树根。',
['p值>x，整棵右子树都太大，只往左。','p值≤x，记录为合法候选，再往右尝试更大值。','走到NULL返回found。'],
'每步被丢弃的子树要么全部非法，要么都不优于已经保存的当前键；因此不会丢最优解。',
'O(h)／O(1)；退化BST仍可能O(n)，不是保证O(log n)。',
'键[2,5,8]，x=6→5；x=1→false；x=8→8；空false。',
'''
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
''','不能无条件返回最后访问点；没有候选要用bool而非特殊整数值；比较边界含等号。')
add('G05','忽略指定顶点后有几个连通块','G1','自编：在遍历中排除一个顶点',
'无向简单图采用邻接表存储，n≥1，给定合法顶点blocked。假想删除该顶点及关联边，求剩余图的连通分量数，不实际修改图。孤立点算一块；原图可不连通。O(V+E)时间、O(V)辅助空间。',
'“删点后连通性但不改结构”把该点预先标成不可进入；其余仍按全图分量遍历。',
'visited同时表示已访问或被排除；外层每次从未访问点发起DFS代表新连通块。',
['visited全零，将blocked标1。','外层枚举其他未访问顶点，启动DFS并令count加1。','DFS只访问未标记邻点，故不会经过blocked桥接两侧。'],
'遍历可使用的顶点和边恰是删点后的图；外层逐次找完各连通分量。',
'O(V+E)／O(V)，含递归栈。',
'链0—1—2删1→2；删端点0→1；只有一个点删除后→0；三角形删任意点→1。',
'''
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
''','不能从外层再次启动blocked；原图本来不连通也要扫描全部点；不是只数blocked的邻点。')
add('G06','用两种颜色检查相邻冲突','G2','保留旧BFS二分染色好题',
'无向简单图采用邻接表存储，允许不连通。判断能否为每点染0或1，使每条边两端异色。空图为真；O(V+E)时间、O(V)空间，不改图。',
'“相邻相反＋可能有环”BFS传播颜色，不是简单按DFS深度取奇偶而不检查已访问边。',
'color=-1未染色；0/1为已确定颜色，兼作访问标记；每个分量任选起点色0。',
['color全部置-1，外层找未染色点。','起点染0并入队；对未染色邻点赋1-color[v]并入队。','若已染色邻点与当前同色，发现冲突；释放工作数组后返回false。'],
'每条边都检查异色约束；若无冲突，最终赋值本身就是合法方案；若冲突则该分量的交替约束不能同时满足。',
'O(V+E)／O(V)。',
'三角形假；四边形真；孤立点真；只有某个后续分量有奇环也是假。',
'''
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
''','int数组={-1}不会全部为-1；入队就染色；不可漏掉已染邻点间的边或后续分量。')
add('G07','依次加入无向边时的冗余边数','G4','旧并查集机制应用化',
'n个编号0..n-1的顶点，按顺序加入m条无向边edges[m][2]。加入一条边前若两端已连通，称其冗余；求冗余边条数。允许重边、自环；n=0时m=0；顶点编号合法。用并查集，不必构造邻接表。',
'“动态加入连接＋问是否已连通”并查集；不是有向可达或最短路。',
'parent按代表根连接；size为根集合大小。只有两端根不同才合并；根相同即冗余。',
['每点独立成集合。','逐边Find两端根。','相同则答案加1，否则小集合挂到大集合并更新大小。'],
'归纳地，集合始终等于已加入边形成的连通块；同根边不增加连通性。',
'路径压缩＋按规模合并：O(n+m·α(n))摊还（n≥1），空间O(n)；空输入常数开销。',
'n=3，边(0,1),(1,2),(0,2),(1,1)→2；重复边第二次起冗余；n=0,m=0→0。',
'''
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
''','必须按根挂接；自环立即同根；并查集不能拿来判有向通路。')
add('G08','非负权矩阵图的单源最短距离','G5','保留一题教材算法兜底，不扩展四套实现',
'有向非负权图用矩阵weight存储，n≥1，源s合法。无边记INF=INT_MAX/4，对角线为0；合法零权边记0；所有有限最短距离保证<INF。将源到各点最短距离写入dist[]，不可达记INF。不改矩阵，O(n²)时间、O(n)额外空间（dist输出另计）。',
'“非负带权最短路”不能用普通BFS层数；用选取未确定最小距离点＋松弛。',
'dist[v]为从源到v的当前最优上界；settled标记距离已最终确定；不是Prim的“接入一条边成本”。',
['dist全INF，源为0；settled全0。','选取未确定且dist最小的u；无有限候选则结束。','确定u，遍历出边，用dist[u]+weight[u][v]改进dist[v]。','重复至无可达候选或最多n次。'],
'非负边保证尚未确定的路径不能绕过更远点再缩短当前最小候选，因此u的距离可确定。',
'O(n²)／O(n)工作空间，输入矩阵O(n²)和dist输出O(n)另列。',
'0→1权0，1→2权2，0→2权5→[0,0,2]；孤立点INF；不能把0当无边。',
'''
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
''','负权不适用；选点是最小dist，不是编号；INF不能当有限边；本题有限量<INF，求和<2INF不会int溢出。')
add('S01','三类括号匹配','S1','仅保留栈基础；兼作最简单字符序列题',
'长度n的字符数组只含()[]{}六种括号，判断是否合法匹配；空序列为真。O(n)时间，可用O(n)栈，不依赖STL。',
'“最近未闭合者最先匹配”后进先出，用栈保存左括号。',
'top=-1为空，stack[0..top]是尚未匹配的左括号。',
['左括号入栈。','右括号时先检查非空，再看栈顶类型是否对应。','对应则弹栈，否则失败；结束必须空栈。'],
'每个右括号只能与最近的未闭合左括号配对；栈精确保存这些左括号。',
'O(n)／O(n)。',
'([{}])真；([)]假；)假；((假；空真。',
'''
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
''','不能只统计左右括号数量；弹栈前检查空；本题输入只含六种括号。')
add('S02','单数字后缀表达式求值','S1','保留基础后缀求值，不设单调栈专题',
'长度n的字符数组由单个数字0..9与二元运算符+、-、*组成，无空格。按后缀表达式求值，合法则通过answer返回int并返回true；非法返回false（此时answer不规定）。保证实际中间运算若发生均不溢出int；空序列非法。O(n)时间、O(n)栈。',
'“运算符在操作数之后”数字压栈，运算时最近两个数出栈。',
'栈存已求值但尚未参与后续运算的部分表达式结果；弹出的第一个是右操作数。',
['数字压栈。','运算符须有至少两个操作数；先弹right，再弹left，结果入栈。','未知字符失败；结束必须恰好剩一个结果。'],
'每个运算符将前面两个已完成子表达式缩成一个值，与后缀表达式递归结构一致。',
'O(n)／O(n)。',
'23-→-1；23+4*→20；2+非法；23非法（多余操作数）；空非法。',
'''
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
''','减法不能反向；有一个结果不代表合法，最终必须恰一个；多位数解析不属于本题。')
add('H01','下滤建大根堆并原地升序排序','H1','保留旧堆基础，将建堆与排序合成一题两步',
'数组A采用0下标，先自底向上建大根堆，再原地升序排序；n可为0。手写下滤与建堆，不使用库；O(1)额外空间，分别分析建堆和排序时间。',
'“堆局部失序”向下调整；“原地升序”反复将最大根放到未排序区末。',
'SiftDownMax调用前，i的左右子树各自已是大根堆；n为当前堆的有效长度，不含已归位后缀。',
['保存根值x，每次选更大的孩子；若x已不小于孩子则停，否则孩子上移。','从n/2-1到0依次下滤建堆。','根与末项交换，缩短堆长，再下滤根。'],
'建堆按子树已成堆的顺序执行；每次交换把剩余最大值放到最终位置，前缀恢复堆后继续。',
'建堆O(n)，排序O(n log(n+1))上界；空间O(1)，下滤为迭代。',
'[3,1,4,1,5]→[1,1,3,4,5]；空、单点、全等、负值；建堆后不一定整体有序。',
'''
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
''','0下标左孩子2i+1；下滤时选较大孩子；排序下滤长度是end而非end+1；建堆不是O(n log n)的紧界。')
add('H02','固定容量保留最大的k项','H1','保留旧Top-k作为选练，不重复扩堆题',
'任意整数数组A长n，0≤k≤n，不得修改A。将最大的k项写入result[]，内部只要求小根堆，不要求排序，重复按项计数。result与输入不重叠且容量≥k。O(n log(k+1)+k)时间，除result外O(1)工作空间；k=0无输出。',
'“保留最大k项”要随时淘汰入选项中最小的那个，所以保留小根堆，不是大根堆。',
'result保存已扫描部分最大的k项；堆根是这些入选项的最弱者。',
['前k项复制并建小根堆。','后续值不大于堆根则跳过；更大就替换根再下滤。','结束保持小根堆，无需再排序。'],
'每次新值只有比当前最小入选值更大才可能改善结果；替换后仍恰保留前缀最大k项。',
'O(k+(n-k)log(k+1))上界，k=0常数返回；result输出占O(k)，其他工作空间O(1)。',
'[3,1,5,2,5]、k=3→多重集[3,5,5]且内部小根堆；k=1取最大；k=0；k=n。',
'''
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
''','最大k用小根堆；result未必升序；输入不改；k=0不能读堆根。')
add('A15','有序数组中的紧密三元组计数','A7','保留旧A11“好题”，修复旧版题答错配',
'非递减整数数组A长n，C≥0。统计下标三元组i<j<k，使|A[i]-A[j]|+|A[j]-A[k]|≤C，重复值按不同下标计数。结果能用long long表示。不改输入，O(n)时间、O(1)空间。',
'“有序＋三个数的跨度限制”先化简绝对值，再固定最右端，窗口内组合计数。不是三数组最小距离，也不是无重复子串。',
'有序保证条件化为A[k]-A[i]≤C；left为固定right时最早合法起点，窗口内除right外有count=right-left个位置。',
['right从0扫描；当跨度>C时while推进left。','此时窗口所有值都落在合法跨度内。','前两个下标从right左侧的count项任选两个，贡献count*(count-1)/2。','累加各right的贡献。'],
'每组三元组有唯一最右下标right；其另外两项只需都处于合法窗口中，组合数既不重也不漏。',
'O(n)／O(1)。',
'[1,2,3,4]、C=2→2；[1,1,1,1]、C=0→4；n<3→0；INT范围端点相减须先提升。',
'''
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
''','旧版此题错贴了最长无重复段代码，本次已重写；按下标计数不可去重；C≥0保证窗口不会越过right。')
add('L11','首尾交替重排原链','L4','保留旧L07及个人断链卡点，作为组合验收',
'带头无环单链表L原序列a1,a2,…,an，重排为a1,an,a2,an-1,…。只能修改next，不能改data或增删结点；O(n)时间、O(1)空间。空表与单点不变。',
'“首尾交替而单链不能后退”拆为找前半尾、断链、逆后半、交替接入。',
'slow为前半尾（奇数前半多一项）；p/q分别为前半/逆后半当前首；交替时先存两边后继。',
['快慢指针定位前半尾。','暂存后半首并slow->next=NULL，确保两段独立。','逆置后半。','以q非空为循环条件，保存nextP/nextQ，接p→q→nextP，再双侧推进。'],
'两半覆盖原序列且不重叠；逆后半给出从末尾向中间的顺序，交替接入即目标排列。',
'O(n)／O(1)。',
'[1,2,3,4,5]→[1,5,2,4,3]；[1,2,3,4]→[1,4,2,3]；空、单点、双点；末尾无环。',
'''
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
''','保留你的原卡点：slow->next要断；交替前两侧都存temp/next；不能边接边失去未处理链。')
TEMPLATES=[]
def template(id,title,signal,ask,state,frame,pitfall):
 TEMPLATES.append(dict(id=id,title=title,signal=signal,ask=ask,state=state,frame=clean(frame),pitfall=pitfall))
template('A1','读写前缀','原地、稳定删除／筛选／压缩','已读部分的结果能否直接放在前缀？',
'A[0..w-1]是已处理结果；r下一读，w下一写，w≤r。',
'''
w = 0
for r = 0..n-1:
    if 保留A[r]: A[w++] = A[r]
return w
压缩重复段时：新值建组；同值只累计频次。
''','无序去重不能只比较相邻项；删除后缀无须清零；返回长度不是末下标。')
template('A2','有序同步推进','已排序的两个序列、匹配／归并／最接近','当前较小项能否被证明不再需要？',
'i,j为两序列未处理首；移动一侧必须有“跳过不损失解”的依据。',
'''
i = j = 0
while i<n and j<m:
    比较A[i],B[j]
    较小侧推进；相等时按任务输出、计数或双侧推进
同一有序数组两数和：才常用一左一右对撞。
''','不存在“求差一律某种双指针”的规则。要看有序性、配对目标与排除依据；排序成本不能漏。')
template('A3','按值标记计数','明确小值域、出现没／出现几次／是否在集合中','槽下标代表值，还是原位置？值域能否承受？',
'seen[v]记成员关系，freq[v]记次数；范围与偏移由题干决定。',
'''
申请M+1槽并清零
for 每个输入x: seen[x]=1 或 freq[x]++
扫描原数据或值域，以标记/次数决定结果
释放数组
''','不能按n盲目当值域；负数需要合法偏移；出现次数与不同值个数别混。')
template('A4','二分边界','有序＋首个满足／最后满足／值域计数，要求对数时间','满足谓词是否在下标上单调？要找哪个边界？',
'闭区间[low,high]尚待判断；answer保留最左合法候选，未找到时为n。',
'''
low=0; high=n-1; answer=n
while low<=high:
    mid=low+(high-low)/2
    if P(A[mid]): answer=mid; high=mid-1
    else: low=mid+1
区间计数 = 首个>highValue - 首个>=lowValue
''','一个查≥，一个查>；不要用最大int+1替代严格边界；不能混写闭区间与半开区间更新。')
template('A5','扫描汇总与历史最优','左右统计、i<j、连续相邻关系、每个位置比较整侧','未来到底需要历史的什么摘要？和、最大值、最小值还是当前段起点？',
'只保存完成任务的最少摘要；当前点是否可以进入摘要必须按下标约束决定。',
'''
切分：先求total；left+=A[i]；右侧=total-left
i<j配对：先用旧best评价j，再把A[j]并入best
两侧判定：预处理rightMin；扫描维护不含当前点的leftMax
连续段：相邻关系断裂则重置start；否则延长
''','这四种同属“扫描保留摘要”，但更新式不一样。先说精确含义，不能只背一个max变量；负数不妨碍前缀恒等式。')
template('A6','划分而非全排序','按阈值分组、第k小、只要最小k项','题目真的要求内部有序或稳定吗？',
'二路划分定位枢轴；三路分区维护<、=、未知、>四段；选择只缩目标所在侧。',
'''
三路：less=i=0, greater=n-1
<：换到less，less++,i++；=：i++；>：换到greater，greater--，i不动
选择：p=Partition(low,high)
p==k-1则停；否则只向包含目标的一侧缩区间
''','分区不等于排序，也不保证稳定；固定枢轴快速选择最坏O(n²)；大于分支交换来的值仍未知。')
template('A7','条件单调的窗口','连续区间、跨度／和限制、移动边界可维护状态','右端加入和左端移出是否有单调性依据？',
'[left,right]与sum/跨度一致；left只前进；答案贡献按当前right计算。',
'''
for right:
    加入右端
    while 需要收缩: 移出左端并left++
    按任务计贡献
最短达标：while仍达标，先记长度再收缩
跨度三元组：恢复合法后，从窗口内前项任选两项
''','普通按和收缩不适用于任意负数；计数与最短长度的更新时机不同；连续段不是子序列。')
template('L1','保存后继再改边','逆置、局部交换、只改next不改值','改这条边之后，未处理部分还能从哪里找到？',
'pre/当前点/暂存next各司其职；头结点通常只作前驱，不参加数据运算。',
'''
逆置：next=p->next; p->next=pre; pre=p; p=next
换一对：pre->a->b->next 变 pre->b->a->next
先画改前/改后边，再按不会丢链的次序赋值
''','只动局部p变量不等于更新头或父链接；解引用前检查存在；尾结点最终必须指NULL。')
template('L2','摘点分流与尾插','稳定分组、归并、保序构造新链','原结点复用还是复制？每条结果链的尾是谁？',
'每组head/tail描述已完成结果；稳定性来自尾插；副本逆序则可有意头插。',
'''
next=p->next; p->next=NULL
选定一组，将p尾插；p=next
多个输入有序：每次取首部较小者；相等先左可保稳定
最后拼接各组，并封尾NULL
''','组内头插会逆序；可复用不代表可共享释放；新建副本的O(n)输出内存要单列。')
template('L3','前驱删除与原始统计','删结点并释放，阈值由原表决定','删除后谁还指向未处理首？判据是否固定来自原表？',
'pre为保留尾，p为待判点；原sum/count先统计且删除中不变。',
'''
若需要原平均值：第一遍统计
pre=L; p=L->next
while p:
    if 删除: pre->next=p->next; delete p; p=pre->next
    else: pre=p; p=p->next
''','删除分支pre不前进；delete后不能读旧p；不能把原表均值变成动态剩余均值。')
template('L4','先定位再组合','中点、共同尾、前后配对、摘出一段、首尾重排','需要定位的是结点、前驱还是一段的两个接口？',
'先只读定位，再做最少改边；复杂任务分为找点→断链→逆置/比较→拼接/恢复。',
'''
对齐共同尾：统计长度；长链先走差值；再同步比地址
中点：快走2慢走1，明确奇数归哪半
摘段：保存段前驱和段尾；前驱绕过段，段尾封NULL
回文/重排：找中点→必要时断链→逆后半→比较或交替→按题意恢复
''','“快慢指针”不是完整解法；恢复要求必须执行，即使比较已失败；共同尾比较地址而非值。')
template('T1','后序向上汇总','高度、规模、孩子结果组合、每个结点的局部条件','父结点需要孩子返回什么？返回给父亲的东西与全局答案是否相同？',
'返回值是当前子树摘要；全局best/count可用引用另传，不能把二者混在一起。',
'''
Solve(p):
    if p==NULL: return 空摘要
    left=Solve(p->lchild); right=Solve(p->rchild)
    用left/right评价当前点并更新答案
    return 本子树摘要
规模L+R+1；高度max(L,R)+1；直径候选L+R但返回高度
''','别对每点重扫子树；“返回高度”不等于“返回最优路径”；外侧规模n-size不能漏。')
template('T2','祖先状态与路径回退','深度、根叶路径、祖先约束、路径和','当前结点缺的信息是否来自祖先？状态按值还是共享？',
'depth/sum按值传可自然回退；共享path长度若引用传就必须失败回退。孩子兄弟先解释语义。',
'''
进入结点：写入path，更新depth/sum
满足终点条件则记录/返回
递归孩子，传更新后的祖先状态
失败离开：撤销共享的path长度
原树兄弟深度相同；孩子深度+1
''','根叶路径必须到叶；有负数不能按超标剪枝；按值参数无需手动减回，共享状态才撤销。')
template('T3','返回并接回新根','删除、收缩、裁剪、子树替换','修改后原根还存在吗？父指针如何拿到新根？',
'函数返回“处理后子树根”；父层必须接住；删除前先保存要保留的孩子。',
'''
if p==NULL: return NULL
p->lchild=Change(p->lchild)
p->rchild=Change(p->rchild)
按当前结点条件，保留p或保存替代孩子、delete p、return child
入口：root=Change(root)
''','不接返回值会留悬空指针；删除后不能再读p；先明确删原叶还是处理后的叶。')
template('T4','BST有序性','中序相邻关系，或按键值找一个边界','要遍历整个有序流，还是只需沿一条搜索路径？',
'中序型：previous跨递归共享，并有hasPrevious；搜索型：candidate是合法最好候选，下一步只选一侧。',
'''
相邻统计：左递归→与previous比较→更新previous→右递归
边界搜索：当前键非法则去更小侧；合法则存候选，再去可能改进侧
先判使用的是严格BST还是允许重复；普通二叉树不能照搬
''','不要用INT_MIN当不存在的哨兵；BST退化时h=n；中序全部遍历与剪枝查找的复杂度不同。')
template('T5','层序与跨层空位','按层、宽度、完全性、层内顺序','本层的结尾在哪里？空位限制是否跨父结点？',
'队列按层推进；层统计开始冻结end=rear；完全性gap一旦出现就不能重置。',
'''
根入队
while 队列非空:
    需要层统计则先冻结end=rear
    按左后右检查孩子、入队
完全性：空孩子令gap=true，之后非空孩子一律失败
''','新入队属于下一层；不能每换父结点清gap；堆还需另查父子大小。')
template('T6','双树同步','两树相等、镜像、结构与数据对应','两个指针该同向配对还是交叉配对？',
'函数责任是“这对根的两棵子树是否满足关系”；两空/恰一空先分类。',
'''
两空true；恰一空false；数据不符false
同树相等：Compare(a左,b左) && Compare(a右,b右)
镜像：Compare(a左,b右) && Compare(a右,b左)
''','单独两份遍历序列可能丢结构；不处理空指针会越界；左右关系不可凭印象。')
template('G1','遍历范围与分量汇总','可达性、连通块、删点后连通、范围内点边统计','只从一个起点，还是扫描全图？沿出边还是反向入边？',
'visited在进入时置1；一次启动负责一块，统计量每块重置；全图标记不重置。',
'''
DFS(v): 标记v；处理v；扫描邻点w，未访问则DFS(w)
全图：for v，若未访问则启动一次DFS并累计块数
反向矩阵：当前v扫描A[u][v]；删点：预先标记为不可进入
''','无向表一条边两项；只计DFS树边不能得真实边数；DFS深度不是一般最短距离。')
template('G2','BFS标号与邻边约束','无权最短路、两侧距离、相邻异色','第一次发现某点时应给它哪个状态？再次遇到要忽略还是检查约束？',
'距离/颜色兼访问标记；入队就赋值，保证每点最多入队一次。',
'''
源赋dist=0或color=0，入队
取v，扫描邻点w
未发现：dist[w]=dist[v]+1 或 color[w]=1-color[v]，入队
已发现：染色题还须检查是否冲突
距离组合：先分别BFS，再按推导出的等式筛选
''','普通BFS不处理任意权重；有向图到终点距离需反向图；“至少一条”和“所有路径”不同。')
template('G3','拓扑消除依赖','有向先后关系、课程并行、DAG状态传播','何时一个点才真正具备处理条件？',
'indegree是剩余未处理前驱数；零入度队列只存当前可处理点；processed用于最终判环。',
'''
统计全部入度，初始0入度入队
取v；对每条v→w减入度，减至0才入队
必要时在出边处传播状态；并行轮次先冻结end=rear
结束：processed<n说明有环
''','有一个源点也可能其他部分有环；学期数不是出队点数；不必物理删除图中的边。')
template('G4','并查集合并','边逐条加入、是否已连通、合并若干等价关系','这是无向连通/集合等价关系吗？',
'parent的根代表集合；只把一个根接到另一个根；size用于按规模合并。',
'''
每点自成集合
对连接u,v：a=Find(u), b=Find(v)
a==b：已连通；否则小根挂到大根并更新size
Find递归返回代表并路径压缩
''','不能当有向可达性、最短路或显式路径；合并失败与新建边数是两回事。')
template('G5','选最小再松弛（备查）','非负权最短路或带权连通代价','目标是源到点的路径，还是把点接进树的一条边？',
'Dijkstra的dist是源路径长；Prim的key是跨当前树集合的一条最便宜连接边。两者不是同一种量。',
'''
Dijkstra：选未确定最小dist[u]，用dist[u]+w(u,v)松弛
Prim：选未入树最小key[u]，用w(u,v)更新连接代价
本套只保留Dijkstra完整练习；Prim/Floyd/Kruskal只识别边界，不铺四套默写
''','非负权前提属于Dijkstra；0权是真边；不能把Prim更新也写成dist[u]+w。未练不代表不在基础知识范围。')
template('S1','后进先出（基础）','最近未完成结构、括号、后缀表达式','后遇到的待处理项是否必须先完成？',
'top=-1为空；括号存未闭合左括号，表达式存已完成子结果。',
'''
入栈：stack[++top]=x
出栈：先判非空，再取stack[top--]
后缀运算：先弹right，再弹left，压回left op right
''','队列先进先出不同；不能只计括号数量；不单设KMP、单调栈等进阶题组。')
template('H1','堆的局部修复（基础）','反复取极值、固定容量候选、堆排序','需要暴露的是全体最大值，还是入选项中最小者？',
'下滤前两棵孩子子树已成堆，只有当前根可能失序；堆有效长度与数组总长度区分。',
'''
保存根x；选合适孩子；若x已满足关系则停，否则孩子上移
最后把x放到停留位置
升序排序用大根堆；保留最大k项用小根堆淘汰最弱者
''','堆不是全局有序；建堆O(n)；下滤长度必须排除已归位后缀；结果缓冲区也占内存。')
assert len(CARDS)==48 and len({c['id'] for c in CARDS})==48
CARDS.sort(key=lambda c: ('ALTGSH'.index(c['id'][0]),int(c['id'][1:])))
TMAP={t['id']:t for t in TEMPLATES}
def cardlink(id,alias=None):
 c=next(c for c in CARDS if c['id']==id)
 return '[['+NAMES[id[0]][:-3]+'#'+id+' '+c['title']+'|'+(alias or id+' '+c['title'])+']]'
def templink(group,alias=None):
 t=TMAP[group]
 return '[['+str(ROOT/TEMPLATE).replace('\\','/')[:-3]+'#'+group+' '+t['title']+'|'+(alias or group+' '+t['title'])+']]'
def quoted(s):return '\n'.join('> '+l if l else '>' for l in s.splitlines())
def render_card(c):
 if 'raw' in c:return c['raw']
 return clean('### '+c['id']+' '+c['title']+'\n\n**来源**：'+c['source']+'''。

- [ ] 首次：能说明状态并独立写出
- [ ] 间隔复写：不看答案通过边界检查

**题干**：'''+c['question']+'\n\n**先手推自测**：'+c['tests']+'\n\n'+quoted('[!faq]- 识别模板、推导与完整代码｜先尝试再展开\n\n**考场识别 → '+templink(c['group'])+'**：'+c['signal']+'\n\n**关键状态**：'+c['state']+'\n\n**解题步骤**\n'+'\n'.join(str(i)+'. '+x for i,x in enumerate(c['steps'],1))+'\n\n**为什么成立**：'+c['reason']+'\n\n**时间／额外空间**：'+c['cost']+'\n\n**易错核对**：'+c['pitfall']+'\n\n**完整核心代码**（本卡单独配公共类型编译）\n\n```cpp\n'+c['code'].strip()+'\n```')+'\n\n**本题卡点**：____；下次先检查：____。\n')

STAGE=CHECK/'staged'
STAGEBASE=STAGE/'练习题'
STAGEBASE.mkdir(parents=True,exist_ok=True)
# Add direct template links to the retained, reviewed pilot analyses.
for c in CARDS:
 if 'raw' in c:
  needle='**考场识别 → '+c['group']+'**'
  c['raw']=c['raw'].replace(needle,'**考场识别 → '+templink(c['group'])+'**')

intro={
'A':('数组与线性表','15题覆盖稳定筛选、有序同步、值域计数、二分边界、历史汇总、原地划分与两道受限窗口。窗口不再占半套题，也不把有序性和线性扫描一并删掉。'),
'L':('链表','11题围绕改边、稳定尾插、前驱删除与定位组合。全部默认带头结点，头不参与数据序列；所有权与是否恢复在题干逐一写明。'),
'T':('树与递归','10题保留第一批4题及其推导，补后序、路径回退、中序、双树与BST剪枝。先决定信息流，再决定访问顺序。'),
'G':('图','8题保留第一批4题，补删点连通、染色、动态合并与一题非负权最短路兜底。基础概念是设计依据，不等于只练历史原题。'),
'S':('栈与字符基础','只留2题：括号匹配与单数字后缀求值。不设独立串专题、KMP题组或单调栈题组；这是本套训练取舍，不是断言它们不会考。'),
'H':('堆基础','只留2题：下滤建堆/堆排序、固定容量Top-k。两题共享下滤机制；H02按需，不与快速选择重复加量。')}
aliases={'T':['408新题训练-01树与递归','04 二叉树模板'],'G':['408新题训练-02图与遍历'],'H':['堆']}
for family in NAMES:
 cards=[c for c in CARDS if c['id'].startswith(family)]
 title,desc=intro[family]
 front=''
 if family in aliases:front='---\naliases:\n'+''.join('  - "'+a+'"\n' for a in aliases[family])+'---\n\n'
 s=front+'# 408代码训练｜'+family+' '+title+'\n\n[[算法分类训练-00总入口|← 总入口]] · [['+str(ROOT/TEMPLATE).replace('\\','/')[:-3]+'|模板总表]] · [[算法分类训练-公共约定|公共类型与接口]]\n\n'+desc+'\n\n'
 s+='## 1. 本页导航\n\n| 题号与任务 | 模板 |\n| --- | --- |\n'
 for c in cards:s+='| '+cardlink(c['id']).replace('|','\\|')+' | '+templink(c['group']).replace('|','\\|')+' |\n'
 s+='\n## 2. 先识别，再展开代码\n\n'
 groups=[t for t in TEMPLATES if t['id'].startswith(family)]
 for t in groups:
  s+='- **'+t['id']+' '+t['title']+'**：'+t['signal']+'。先问：'+t['ask']+'\n'
 s+='\n模板是可组合机制，不是互斥题名；解答内有框架与不变量链接。练习时先自行说出模板和状态，再看FAQ；熟悉后遮住上方导航做混合验收。\n\n'
 if family=='G':
  s+='> [!tip] 度数扫描按需回补，不另算正式题\n> 有向邻接表中，从v的表头逐项扫描，每个邻接项使outdegree[v]和indegree[adjvex]各加1；两数组先全零。复杂度O(V+E)，不是对每对顶点试一次。无向邻接表每条边保存两个邻接项，不能拿邻接项总数直接当边数。\n\n'
 for c in cards:s+=render_card(c)+'\n'
 s+='## 3. 复写只留一行\n\n识别错在：____；状态错在：____；改边／更新时机错在：____。\n\n旧题号与本页题号可能不同，不能据旧勾选当作本页已通过。历史作答与完整原文均在trash字节归档，恢复方法见[[算法分类训练-整理与校验记录]]。\n'
 write(STAGEBASE/NAMES[family],s)

s='# 408代码模板｜考场识别与框架速查\n\n[[算法分类训练-00总入口|← 训练总入口]] · [[算法分类训练-公共约定|类型与代码约定]]\n\n'
s+='> [!important] 模板只背到可推导，不背48份代码\n> 考场第一步：**给了什么结构和性质 → 要做什么动作 → 哪些状态够用 → 写最小骨架**。本页将旧版框架调整为24张识别卡，归在数组、链表、树、图与栈堆基础中；它们可以组合，不是24条互斥暗号，也不是24份当天都要背完的代码。\n\n'
s+='## 1. 一眼分派：先选机制，再看小类\n\n| 结构 | 题面信号 | 首选机制 |\n| --- | --- | --- |\n'
for family in ['A','L','T','G','S','H']:
 for t in TEMPLATES:
  if t['id'].startswith(family):s+='| '+family+' | '+t['signal']+' | '+templink(t['id']).replace('|','\\|')+' |\n'
s+='\n## 2. 四句考场起手式\n\n1. **约束**：有序吗、值域多大、是否非负、只读还是可修改、要不要稳定？\n2. **职责**：当前函数处理哪个范围，输入和返回值精确是什么？\n3. **状态**：哪些来自历史／祖先，哪些等孩子返回，谁共享、谁要回退？\n4. **成本**：一项或一条边会被处理几次，输出与递归栈要不要另计？\n\n**不能识别时先写朴素法，再问哪个重复扫描可用摘要或性质消掉。** 信号必须有条件支持；“两个指针”“一次递归”本身都不是完整算法思想。\n\n## 3. 24张识别卡\n\n以下框架用伪代码概括处理顺序，不是可直接编译的答案。完整可编译代码在链接题卡中。\n\n'
for t in TEMPLATES:
 cs=[c for c in CARDS if c['group']==t['id']]
 s+='### '+t['id']+' '+t['title']+'\n\n**识别信号**：'+t['signal']+'。\n\n**先问自己**：'+t['ask']+'\n\n'
 s+=quoted('[!faq]- 框架与状态｜先闭卷说，再展开\n\n**关键状态／不变量**：'+t['state']+'\n\n```text\n'+t['frame'].strip()+'\n```\n\n**不能套错**：'+t['pitfall'])+'\n\n'
 s+='**对应练习**：'+' · '.join(cardlink(c['id'],c['id']) for c in cs)+'。\n\n'
s+='## 4. 常见组合，不再另背整套\n\n'
for id,phrase in [('A07','A3成员标记＋A1稳定筛选'),('A15','A7跨度窗口＋组合计数'),('L07','L4找中点＋L1逆置＋比较＋恢复'),('L11','L4定位断链＋L1逆置＋局部穿插'),('T03','T5完全性空位＋堆的局部父子约束'),('T04','T1子树规模＋固定总量求外侧'),('T06','T2向下传和＋共享路径失败回退'),('G04','G2两次距离标号＋等式筛选'),('G03','G3拓扑删除＋队列冻结层边界')]:
 s+='- '+cardlink(id)+'：**'+phrase+'**。\n'
s+='\n## 5. 看到这些情况，先停止套模板\n\n- 无序输入却打算直接用有序两指针：先说明能否排序及其代价。\n- 数组含负数却打算按和收缩：单调性可能失效；前缀恒等式则仍可用。\n- 共享链表结点却打算删除或分别释放：先确认所有权。\n- 删除树结点却没有新根返回通道：父链接可能悬空。\n- 一般图拿DFS深度当最短路，或有权图直接BFS：目标状态不符。\n- “未考过”被当成一定不会／一定简单：不是算法适用条件。\n\n## 6. 每天练完只补这一个空\n\n> 题面里的 **____条件** 让我选 **____模板**；我维护 **____状态**；一轮结束仍成立因为 **____**。\n\n能说模板名但解释不出状态，不算真正识别；能写代码却换个题面就认不出，回到本页的识别信号与对应组合，而不是再抄一遍整题。\n'
write(STAGE/TEMPLATE,s)
# Reuse the established public type definitions without touching archived source bytes.
old_public=(BASE/PUBLIC).read_text(encoding='utf-8')
common=next(b for b in re.findall(r'```cpp\n(.*?)\n```',old_public,re.S) if 'typedef struct BTNode' in b)
public=clean('''
# 408代码训练｜公共约定

[[算法分类训练-00总入口|← 总入口]] · [[算法分类训练-整理与校验记录|整理与测试记录]]

## 1. 本套代码口径

使用C++17可编译的基础C/C++教材风格：数组、指针、结构体、必要引用参数；核心答案不依赖STL。**这是一致的训练约定，不是声称考试只允许此写法，也不代替原题要求。**

考场按“算法思想 → 核心函数及必要辅助函数 → 时间／空间”输出，不要求写main和测试造数。每题核心代码都完整展开；每张题卡独立配所需公共类型编译，不能将重复辅助函数整页拼接。

## 2. 公共类型

```cpp
''')+common+'\n```\n\n'+clean('''
- 数组默认0下标，长度是有效元素数；实际容量在题干另行保证。out[]等调用者输出缓冲区默认与输入、其他输出不重叠，除非题干明确原地写回。
- 链表默认带头结点：L本身非NULL，首数据结点L->next，空表L->next==NULL。头不计长度，不参与数据运算。无环，除共享尾题外不同输入链不共享数据结点。
- 修改或删除结点题由new创建且有独占所有权；delete只释放指定结点，不会自动释放后继。共享尾题不得删除或按两份独立链重复释放。
- 普通树BTNode使用data/lchild/rchild；空树NULL，高度按结点层数（空0、叶1），深度按边数（根0）。孩子兄弟题内另定义CSNode，不能把nextsibling当普通右孩子。
- 邻接表：firstarc是第一条出邻接项，adjvex为相邻顶点编号，nextarc接同一顶点其他邻接项。0≤vexnum≤MAXSIZE，编号合法。无向边保存两个邻接项；arcnum记边数，不记邻接项数。
- 矩阵题明示A[u][v]含义；0/1可达矩阵与带权矩阵不是同一约定。带权图零权边合法，INF才表示无边。

## 3. 命名与状态

| 名称 | 职责 |
| --- | --- |
| A/B,n/m | 数组与实际长度 |
| low/high/mid | 二分或划分闭区间及中点 |
| front/rear | 队列下一出队／下一入队位置，空时相等 |
| stack/top | 顺序栈，top=-1为空；入stack[++top]，出stack[top--] |
| p/q/pre/next | 当前点、另一游标、前驱、暂存原后继；题内补充具体职责 |
| out/count | 输出缓冲区与实际写入项数 |
| visited/dist/color | 访问标记／距离／颜色；不能笼统混成“标记” |
| indegree/outdegree | 剩余入度或原入出度，题内说明是否在变化 |

引用如int &length表示调用者共享状态；按值参数如sum、depth在递归返回后自动恢复，不必手动减。引用路径长度若改变，失败分支必须回退。

## 4. 分配、数值和复杂度

```cpp
int *q = new int[n]();  // n个int置0；若需要-1须逐项赋值
// 使用完毕
 delete[] q;
```

- 有固定上限可用MAXSIZE；不是所有数组都必须动态申请。`new`对应`delete`，`new[]`对应`delete[]`；不混用malloc/free。
- 动态数组零初始化本身有线性时间成本，提前返回不能无视这部分。int A[N]={-1}不是全填-1，只有第0项为-1，其余0。
- 差、和、乘积需先提升类型：例如(long long)a-b、(long long)data*count，不能int溢出后才转换。题干保证要求的long long运算可表示；规模和容量合法、分配成功。
- bool成功标志与结果分离，避免INT_MIN、-1等合法数据冒充不存在；只有明确范围之外的哨兵才可用。
- 额外空间计入递归栈。普通树O(h)，退化h=n；不能默认O(log n)。输入存储、调用者输出与工作空间分别说明，新建结果结点仍占内存。
- “最小k项”不要求内部排序；快速选择固定枢轴最坏O(n²)，建堆O(n)，堆排序最坏O(n log n)。算法标签不是复杂度证明。

## 5. 新旧记录

正式训练共48题，状态以各题两个空勾选独立记录；旧完成、得分和批注没有自动迁成新题已完成。旧原文逐字节归入Obsidian本地trash；恢复清单与个人卡点摘要见[[算法分类训练-整理与校验记录]]。
''')
write(STAGEBASE/PUBLIC,public)

def full_template_link():return '[['+str(ROOT/TEMPLATE).replace('\\','/')[:-3]+'|03算法题模板：识别与框架]]'
entry=clean('''
---
aliases:
  - "408新题训练-00树图样稿入口"
---
# 408代码训练｜模板识别与新题应用

> [!important] 当前正式主线（2026-11-06整合）
> **识别题面条件 → 选可组合模板 → 说出状态 → 写代码 → 核对边界。** 旧模板升级为24张识别卡，题目整合为48道：数组15、链表11、树10、图8，另留栈2、堆2作基础备查。不是48份答案死记，也不是48题必须清空。
''')+'\n**先打开 '+full_template_link()+'。**\n\n'+clean('''
## 1. 日常只用这三个层级

1. **总入口**：选一个当前薄弱机制，不再同时开多套周计划。
2. **模板总表**：先遮住框架，说识别信号／状态／处理次序，再核对。
3. **对应题卡**：题干先做，FAQ后看；卡住回到该模板，不把整专题重刷当惩罚。

来源、旧资料恢复与真实编译范围：[[算法分类训练-整理与校验记录]]。类型与接口：[[算法分类训练-公共约定]]。

## 2. 专题入口

| 专题 | 题量 | 模板 | 入口 |
| --- | --- | --- | --- |
| 数组 | 15 | A1–A7，筛选／有序／值域／二分／汇总／划分／受限窗口 | [[算法分类训练-01-A数组与线性表]] |
| 链表 | 11 | L1–L4，改边／分流尾插／前驱删除／定位组合 | [[算法分类训练-02-L链表]] |
| 树 | 10 | T1–T6，后序／路径／新根／BST／层序／双树 | [[算法分类训练-03-T树与递归]] |
| 图 | 8 | G1–G5，遍历／BFS／拓扑／并查集／带权备查 | [[算法分类训练-05-G图]] |
| 栈 | 2 | S1，括号／基础后缀求值 | [[算法分类训练-04-S栈与队列]] |
| 堆 | 2 | H1，下滤建堆／Top-k备查 | [[算法分类训练-06-H堆与排序]] |

保留第一批已认可的树图8题及其主要推导；旧好题也可重写保留。来源逐题注明，“自编”不保证全网从未出现，更不标出题概率。

## 3. 下一次可以直接这样练
''')+'\n'
for phrase,id in [('熟悉读写前缀但需要快速进入', 'A01'),('先练新数组任务','A08'),('练指针重接','L06'),('链表组合验收','L08'),('保持第一批出题方向','T02'),('图的组合验收','G04')]:
 entry+='- '+phrase+'：'+cardlink(id)+'。\n'
entry+='\n'+clean('''
## 4. 约40天的用法，不要求刚好40题

| 阶段 | 练法 | 达到什么程度 |
| --- | --- | --- |
| 前5次练习 | 每次先回忆一个模板，再做1道代表题 | 说清状态，能写基础框架 |
| 接下来的主要时段 | 通常每天1道，交替数组／链表／树／图；已会的基础不反复占天数 | 独立完成思路、代码、复杂度与边界 |
| 距结束约10次练习 | 不看模板导航，混合抽组合题；每次先用1分钟写“信号→模板→状态” | 换题面仍能识别，可组合机制 |
| 最后约5次 | 集中回看模板表和自己的失败点，复写曾卡住的题；少开新题 | 快速提取框架，不靠记住题面 |

这只是约40天的使用方式，不绑定未经核实的考试日期，也不意味着48题全做后才能回看。一次通常30–45分钟，难题可拆两次；第二天优先补昨天的状态／改边错误，而不是为了每天换题硬推进。

- 栈和堆只留基础；S02、H02及G08可按需备查，不与主线叠加成新负担。
- 不单设串题组：基础字符处理放在栈两题中；没练KMP不等于断言串不在考试范围。
- 排序保留划分、选择和堆基础，不另铺大量完整排序默写；带权图仅一题兜底，不铺四套实现。

## 5. 混合识别题签：只看任务先选框架

下面FAQ的标题只给任务，不给模板。先口述识别，再展开找对应练习。
''')+'\n'
for title,ids,ans in [
 ('原地保序删掉另一无序集合里出现的值',['A07'],'值域标记＋读写前缀'),
 ('从原链摘出最优连续一段，剩下仍成链',['L08'],'先只读定位段前驱和尾，再摘链'),
 ('对树每个结点分析去掉它后各部分有多大',['T04'],'后序规模＋固定总量补外侧'),
 ('有向图哪些点能到同一个终点',['G02'],'反转问题方向，矩阵扫描列'),
 ('找出属于某条两端最短路的全部顶点',['G04'],'两端BFS距离＋条件筛选'),
 ('首尾交替排列一条单链，不改数据',['L11'],'中点断链＋逆后半＋交替接入'),
 ('BST中找一个不越界的最大候选',['T10'],'沿一条路径维护合法最优候选'),
 ('有序值形成三元组，但只限制跨度',['A15'],'化简绝对值＋窗口＋组合计数')]:
 entry+=quoted('[!faq]- '+title+'\n\n'+ans+'。对应：'+'、'.join(cardlink(i) for i in ids)+'。')+'\n\n'
entry+=clean('''
## 6. 一行卡点，反哺模板

> 题面中的____让我选____；状态应为____；我错在____（识别／初始化／更新时机／断链／回退／边界）。

旧个人提示保留在整理记录：特别是链表断链与temp、图遍历与距离、堆下滤。旧勾选没有被伪装成本套新题已经掌握。
''')
write(STAGEBASE/ENTRY,entry)

# Collect historic completion lines accurately (not occurrences like freq[x] inside code).
history=[]
for relative in ['练习题/算法分类训练-改写前留档-2026-11-05/原版-算法分类训练-01-A数组与线性表.md','练习题/训练第1周-混合保温.md']:
 heading=''
 for line in (ROOT/relative).read_text(encoding='utf-8').splitlines():
  if line.startswith('#'):heading=re.sub(r'<[^>]+>','',line).lstrip('# ').strip()
  if re.match(r'^\s*- \[[xX]\]',line):history.append([relative,heading,line])
write(CHECK/'history-summary.json',json.dumps(history,ensure_ascii=False,indent=2))
record=clean('''
# 408代码训练｜整合、历史保留与校验记录

[[算法分类训练-00总入口|← 总入口]]

## 1. 本次做了什么（2026-11-06）

将“真题型主练”与树图样稿整合成一套正式材料：1份总入口、1份模板总表、6份专题、1份公共约定和本记录，共10份Markdown。模板总表保留在上一级03算法题模板，其余9份在练习题目录。

**48道题**：数组15、链表11、树10、图8、栈2、堆2。**24张识别卡**：数组7、链表4、树6、图5、栈堆各1。模板用于识别和组合，不推算命题概率；框架是说明处理次序的伪代码，不冒称可直接编译。

第一批树图8题已被认可，全部保留主要推导与代码，NT01–NT04变为T01–T04，NG01–NG04变为G01–G04。其他旧题按价值保留或升级，不按“没有直接真题对应”一律暂缓。新题号不等于旧题号，不能直接继承已完成状态。

## 2. 相对旧版的关键修正

- 从“按真题题型复练”恢复到“信号→机制→状态→框架→应用题”。不要求先做完已考原题才能练迁移。
- 数组仍保留有序性、划分、线性扫描；窗口压为两道有条件的代表，不再大量堆近似计数题。
- 旧A11“紧密三元组”曾错贴无重复段代码；本次保留好题为A15，重新化简绝对值并写窗口组合计数。
- 删除旧模板中“求差必须某种双指针”的绝对句：移动规则由有序性及排除证明决定，不由“和／差”字面决定。
- 链表统一带头结点，逐题明确是否复用、是否删除、是否共享、是否恢复；辅助逆置完整展开。
- 树同时覆盖向上、向下、改结构、BST、层序和双树，不把树练习缩成WPL／表达式树／BST几道旧题。
- 图覆盖遍历、距离、依赖、集合合并；只留一题Dijkstra兜底，不铺四套最短路／生成树实现。
- 栈堆压到各两题，不单开串和单调栈进阶题组。这是训练投入取舍，不是判断“首次出现一定简单”。

## 3. 设计依据与证据边界

历年题型与个人得分来自KK此前提供的清单；旧清单全文在trash归档。本次没有逐年取得2009—2026原卷全文，因此不写“这些题历年从未考过”，更不根据结构轮换押题。“自编”表示本次组织任务，不保证全网原创。

基础范围参照此前核验的高教社《全国硕士研究生招生考试计算机学科专业基础考试大纲解析》公开目录（2025年10月出版，ISBN 978-7-04-065779-1），涉及线性表、树、图、查找、排序等。2027版大纲出版信息此前已核验，但未取得其全文，本次不声称逐条对齐所有新增删改。题目风格是教材式基础C/C++，不冒充官方唯一答案。

## 4. 个人记录没有被清空

以下是历史摘要，不自动勾选本套题目：

- 旧数组专题已有若干首次完成：有序去重、稳定删除、两数配对、数对计数、非负窗口、最短达标、最小缺失正数等。完整勾选与当时答案保存在原文件，不拿它替代新题复写。
- 第1周记录中的原话：**“slow->next 需断链，交替接入不熟。应引入 temp。”** 对应本套L11，题内也保留此提示。
- 原第1周无权最短路径条数标“不会”、最大连通块标“不熟”：本套先用G01/G04补遍历状态和距离，不强制重开计数变式。
- 原第1周小根堆下滤标“没做出来”：本套H01/H02保留基础下滤与用途辨析。
- 原“单调栈冷门”等个人标注连同原代码保存在trash；未把它们转成新的任务。

精确历史已勾选行及其原题标题保存在当前校验目录history-summary.json。用户原代码、颜色批注、所有旧Markdown与旧验证脚本按字节保留，不只保存这个摘要。

## 5. trash迁移与恢复

使用Obsidian本地trash，不永久删除。归档根：

```text
.trash/408算法训练-整合前-2026-11-06/
```

保留原08算法题目录内相对层级：被重写的10份原文件先备份到此处，其他旧题单、周计划、旧模板单页、旧留档、树图样稿和前两轮校验目录整体移入同一归档。只清理08算法题范围，不移动其他数据结构章节。

当前隐藏校验目录为练习题/.408-integrated-check-2026-11-06，保存修改前SHA-256清单、生成数据、测试与审计脚本。归档中原文件名和原字节不改，以免破坏用户代码与批注。历史文件内部旧链接仅在恢复原层级时继续成立；它们不再是当前导航。

需要恢复单份历史文件时，使用校验目录restore.py查看列表或复制到新的恢复文件夹。脚本只复制、不覆盖、不删除当前文件；不要把归档整套直接盖回正式材料。

**链接核验边界**：本次核验10份正式笔记和05数据结构范围内对这批文件的引用；不扫描全vault，因此不能声称库外所有硬编码旧链接均已核验。保留常用文件名并为树图样稿及旧树／堆页加aliases辅助查找；带旧绝对层级的链接仍可能需要手工定位。

## 6. 逐题来源和模板
''')+'\n| 当前题 | 来源 | 模板 |\n| --- | --- | --- |\n'
for c in CARDS:record+='| '+cardlink(c['id']).replace('|','\\|')+' | '+c['source'].rstrip('。')+' | '+c['group']+' |\n'
record+='\n## 7. 实际校验\n\n待完成后以真实测试结果回填。\n'
write(STAGEBASE/RECORD,record)
write(CHECK/'cards.json',json.dumps(CARDS,ensure_ascii=False,indent=2))
write(CHECK/'templates.json',json.dumps(TEMPLATES,ensure_ascii=False,indent=2))
write(CHECK/'common.hpp',common+'\n')
print(json.dumps({'cards':len(CARDS),'templates':len(TEMPLATES),'staged_notes':len(list(STAGE.rglob('*.md'))),'family_counts':{f:sum(c['id'][0]==f for c in CARDS) for f in NAMES}},ensure_ascii=False,indent=2))