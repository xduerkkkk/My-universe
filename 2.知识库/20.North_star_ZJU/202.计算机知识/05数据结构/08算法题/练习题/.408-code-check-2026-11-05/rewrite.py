from pathlib import Path
import re, json, hashlib, textwrap
P = Path('2.知识库/20.North_star_ZJU/202.计算机知识/05数据结构/08算法题/练习题')
WORK = P / '.408-code-check-2026-11-05'
BACK = P / '算法分类训练-改写前留档-2026-11-05'
NAMES = [
 '算法分类训练-01-A数组与线性表', '算法分类训练-02-L链表',
 '算法分类训练-03-T树与递归', '算法分类训练-04-S栈与队列',
 '算法分类训练-05-G图', '算法分类训练-06-H堆与排序']
originals = {f.name: f.read_bytes() for f in P.glob('算法分类训练-*.md')}
if BACK.exists():
 raise RuntimeError('留档目录已经存在；停止，避免覆盖已有留档或用户改动。')
BACK.mkdir()
manifest = {}
for name, data in originals.items():
 (BACK / ('原版-' + name)).write_bytes(data)
 manifest[name] = hashlib.sha256(data).hexdigest()
# Also record untouched pre-existing study material within this directory, not elsewhere in the vault.
untouched = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in P.glob('*.md') if f.name not in originals}
(WORK/'before-manifest.json').write_text(json.dumps({'changed':manifest,'untouched':untouched},ensure_ascii=False,indent=2),encoding='utf-8')
old = {k:v.decode('utf-8-sig') for k,v in originals.items()}
sections = {}
old_heads = {}
for name in NAMES:
 s=old[name+'.md']
 old_heads[name]=re.findall(r'^#{2,3} (.+)$',s,re.M)
 for m in re.finditer(r'^### ([ALTHSG]\d{2}) ([^\n]+)\n(.*?)(?=^## |^### |\Z)',s,re.M|re.S):
  qid,title,body=m.groups()
  checks=re.findall(r'^- \[[ xX]\].*$',body,re.M)
  assert len(checks)==2,(qid,checks)
  sections[qid]={'title':title,'body':body,'checks':checks,'file':name}
assert len(sections)==72,len(sections)
cards={}
def card(qid,title,level,source,prompt,tests,states,steps,code,cost,trap,trace=''):
 assert qid not in cards
 cards[qid]=dict(id=qid,title=title,level=level,source=source,prompt=prompt,tests=tests,states=states,steps=steps,code=textwrap.dedent(code).strip(),cost=cost,trap=trap,trace=trace)

card('A01','有序数组原地去重','基础积木','读写指针；不是新增冲刺任务',
 '非递减整数数组 A，长度 n≥0。原地去重，每种值只留一个，返回有效长度。',
 '[1,1,2,2,3] → 3，前3项为[1,2,3]；[] → 0；[2,2] → 1。',
 '`i` 扫描原数组；`k` 是已保留元素个数，也就是下一个写入位置。',
 ['从左到右读 A[i]；A[0..k-1] 始终是已去重的有效段。','没有保留过元素，或当前值不等于最后保留值时，把它写到 A[k]。','写入后 k 加1；最终返回 k，而不是原长度 n。'],
 '''
 int Unique(int A[], int n) {
     int k = 0;  // 已保留元素个数
     for (int i = 0; i < n; i++) {
         if (k == 0 || A[i] != A[k - 1]) {
             A[k] = A[i];
             k++;
         }
     }
     return k;
 }
 ''','O(n) / O(1)。','k==0 时不能先读 A[k-1]；数组本来就必须有序。')
card('A02','稳定删除指定值','基础积木','读写指针',
 '从整数数组 A 中删除所有等于 x 的元素，保持其余元素相对顺序；原地完成，返回新长度。',
 '[2,1,2,3]，x=2 → 2，前2项[1,3]；全删 → 0；空数组 → 0。',
 '`i` 负责读；`k` 表示已经留下多少个不等于 x 的元素。',
 ['逐项检查 A[i]。','等于 x 就跳过；不等于 x 就写入 A[k]，然后 k++。','只把前 k 项当作删除后的结果，后面的旧数据不必清零。'],
 '''
 int RemoveValue(int A[], int n, int x) {
     int k = 0;
     for (int i = 0; i < n; i++) {
         if (A[i] != x) {
             A[k] = A[i];
             k++;
         }
     }
     return k;
 }
 ''','O(n) / O(1)。','删除的是逻辑长度，不需要为每个待删元素都整体左移一次。')
card('A12','最小未出现正整数','主练','2018·41：按用户给出的题型改写',
 '给定长度 n≥0 的整数数组 A，可含负数、0和重复值。不改 A，允许 O(n) 辅助空间，求未出现的最小正整数。',
 '[3,4,-1,1] → 2；[1,2,3] → 4；[0,-2] → 1；[] → 1。',
 '`visited[x]` 表示正整数 x 是否出现；只关心 1..n。',
 ['长度为 n，答案一定落在 1..n+1；若1..n全在，答案才是 n+1。','申请 n+1 个标记，全部置0；下标0不用。','扫描 A，只给 1≤A[i]≤n 的值打标记。','从1向上找到第一个未出现值；返回前释放辅助数组。'],
 '''
 int FirstMissingPositive(const int A[], int n) {
     int *visited = new int[n + 1]();
     for (int i = 0; i < n; i++) {
         if (A[i] >= 1 && A[i] <= n) {
             visited[A[i]] = 1;
         }
     }
     int answer = n + 1;
     for (int x = 1; x <= n; x++) {
         if (visited[x] == 0) {
             answer = x;
             break;
         }
     }
     delete[] visited;
     return answer;
 }
 ''','O(n) / O(n)（n=0 时只申请1格）。','不能把负数或大于 n 的数直接拿来当下标；这里不需要原地置换的另一套技巧。',
 '[3,4,-1,1]，n=4：标记1、3、4，从1检查，在2处首次遇到0。')
card('A16','二分查找左右边界','基础积木','闭区间二分；本次针对选中文段重写',
 '非递减数组 A，长度 n≥0。分别返回第一个≥x、第一​​个>x 的下标；不存在返回 n。',
 '[1,2,2,4]，x=2 → 1、3；x=0 → 0、0；x=5 → 4、4；空数组 → 0、0。',
 '`[low,high]` 是待查闭区间；`answer` 是目前找到的最靠左候选，下标 n 表示还没找到。',
 ['low=0、high=n-1、answer=n；空数组自然不进入循环。','A[mid] 满足条件时，先记住 mid，再到它左边找更早的候选。','不满足时，mid 及其左侧都不可能满足，令 low=mid+1。','两个函数只差一个条件：≥x 与 >x。'],
 '''
 int LowerBound(const int A[], int n, int x) {
     int low = 0;
     int high = n - 1;
     int answer = n;
     while (low <= high) {
         int mid = low + (high - low) / 2;
         if (A[mid] >= x) {
             answer = mid;   // 记住候选，但继续向左找
             high = mid - 1;
         } else {
             low = mid + 1;
         }
     }
     return answer;
 }

 int UpperBound(const int A[], int n, int x) {
     int low = 0;
     int high = n - 1;
     int answer = n;
     while (low <= high) {
         int mid = low + (high - low) / 2;
         if (A[mid] > x) {
             answer = mid;
             high = mid - 1;
         } else {
             low = mid + 1;
         }
     }
     return answer;
 }
 ''','O(log(n+1)) / O(1)。','本页不用 [low,high) 的另一套边界约定；返回 n 后不能读取 A[n]。x 的个数为 UpperBound-LowerBound。',
 'A=[1,2,2,4]、x=2，找左边界：mid=1 满足，先记 answer=1，再把 high 改成0；检查下标0后结束，返回1。')
card('A18','Partition 与第 k 小','主练','2022·42：最小 k 个数；本卡补齐与旧题“第k小”的联系',
 '长度 n≥1，1≤k≤n，允许修改 A。先写第 k 小，再使 A 的前 k 项成为最小 k 个数（内部不要求有序）。',
 '[4,1,3,2]，k=2 → 第2小为2，前2项集合{1,2}；[2,2,1]，k=2 → 2；k=n → 全部。',
 '`pivot` 是枢轴值；划分后枢轴下标为 pos；`k-1` 是第 k 小在排序结果中的下标。',
 ['一次划分把枢轴放到最终秩位置，左边≤它，右边≥它。','若 pos=k-1 已找到；pos 太大只查左段，太小只查右段。','反复缩小闭区间，不对不需要的一侧排序。','找到后前 k 项就是最小 k 个数，但它们内部仍可能无序。'],
 '''
 int Partition(int A[], int low, int high) {
     int pivot = A[low];
     while (low < high) {
         while (low < high && A[high] >= pivot) {
             high--;
         }
         A[low] = A[high];
         while (low < high && A[low] <= pivot) {
             low++;
         }
         A[high] = A[low];
     }
     A[low] = pivot;
     return low;
 }

 int SelectK(int A[], int n, int k) {
     int low = 0;
     int high = n - 1;
     while (low <= high) {
         int pos = Partition(A, low, high);
         if (pos == k - 1) {
             return A[pos];
         }
         if (pos > k - 1) {
             high = pos - 1;
         } else {
             low = pos + 1;
         }
     }
     return 0;  // 合法的 n、k 不会走到这里
 }

 void SmallestK(int A[], int n, int k) {
     SelectK(A, n, k);  // 前 k 项即为答案，不要求内部有序
 }
 ''','随机排列等平均分析前提下 O(n)，最坏 O(n²) / O(1)，此实现不使用递归。','第 k 小对应下标 k-1。首元素作枢轴并不保证每次折半；不能写“严格 O(n)”或“前 k 项已排序”。')
card('A19','人数最均衡且总和差最大的分组','主练','2016·43：按用户题型改写；允许负数，并明确奇数长度',
 'n≥2，把全部元素分为两组，人数之差≤1，使两组总和的绝对差最大。允许修改数组，只返回最大差，不要求最后数组一定保留最优分组布局。',
 '[1,2,3,4] → 4；[-100,-99,1] → 200；[5,5] → 0。',
 '`k=n/2` 是较小组人数；`total` 为总和；选 k 个数的和为 s 时，两组差为 |total-2s|。',
 ['先写完整 Partition/SelectK；下面已在本卡展开，不需跳到别处补代码。','用快速选择把最小 k 个放到前面，计算这一极端的差。','若 n 为偶数，另一个极端只是交换两组，直接返回。','若 n 为奇数，还要检查最大 k 个组成较小组的情况；两种差取较大值。'],
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

 int SelectK(int A[], int n, int k) {
     int low = 0;
     int high = n - 1;
     while (low <= high) {
         int pos = Partition(A, low, high);
         if (pos == k - 1) return A[pos];
         if (pos > k - 1) high = pos - 1;
         else low = pos + 1;
     }
     return 0;
 }

 long long BalancedDifference(int A[], int n) {
     int k = n / 2;
     long long total = 0;
     for (int i = 0; i < n; i++) total += A[i];

     SelectK(A, n, k);
     long long smallSum = 0;
     for (int i = 0; i < k; i++) smallSum += A[i];
     long long answer = total - 2 * smallSum;
     if (answer < 0) answer = -answer;
     if (n % 2 == 0) return answer;

     SelectK(A, n, n - k);
     long long largeSum = 0;
     for (int i = n - k; i < n; i++) largeSum += A[i];
     long long other = total - 2 * largeSum;
     if (other < 0) other = -other;
     if (other > answer) answer = other;
     return answer;
 }
 ''','快速选择的平均分析前提下 O(n)，最坏 O(n²) / O(1)。','奇数 n、允许负数时，不能只检查最小 k 个；这不是背一条“排序后对半切”就结束。long long 中间运算必须可表示。',
 '[-100,-99,1]：较小组只有1人。选-100，差2；选1，差200，所以负数情况下必须比较两个极端。')
card('A20','后缀最大乘积（允许自身）','主练','2025·41：用户给出的是题型标题，未提供原题的 j 范围；本卡沿用 i≤j 的训练定义',
 '整数数组 A 可含正、负、0。求 result[i]=max{A[i]×A[j]｜i≤j<n}，允许自身；不改 A，输出与 A 不重叠。n≥0，乘积能用 long long 表示。原题若要求 i<j，改练留档中的 A21，不把两种定义混用。',
 '[-3,2,-4] → [12,4,16]；[0,-2] → [0,4]；[] → []。',
 '`suffixMin/suffixMax` 记录已纳入后缀的最小值/最大值；本题先纳入 A[i]，再计算答案。',
 ['从右向左扫描；因为 j≥i，所以先把当前值放入后缀极值。','A[i]≥0 时，乘后缀最大值最好。','A[i]<0 时，乘后缀最小值最好，负负可以得正。','每步只保留两个极值，不必保存整个后缀；结果数组不算辅助工作空间。'],
 '''
 void SuffixMaxProduct(const int A[], int n, long long result[]) {
     if (n == 0) return;
     int suffixMin = A[n - 1];
     int suffixMax = A[n - 1];
     for (int i = n - 1; i >= 0; i--) {
         if (A[i] < suffixMin) suffixMin = A[i];
         if (A[i] > suffixMax) suffixMax = A[i];
         if (A[i] >= 0) {
             result[i] = (long long)A[i] * suffixMax;
         } else {
             result[i] = (long long)A[i] * suffixMin;
         }
     }
 }
 ''','O(n) / O(1) 辅助空间，另有 O(n) 输出空间。','不能只维护后缀最大值；允许自身要先更新，禁止自身要先查询。两者最后一项的合法性不同。',
 '[-3,2,-4] 从右扫：-4的后缀极值均为-4，得16；2的后缀最大为2，得4；-3的后缀最小为-4，得12。')
card('A24','数组循环左移','主练','2010·42：按用户给出的题型改写',
 '长度 n≥0 的数组 A 循环左移 p 位，p≥0。要求 O(n) 时间、O(1) 辅助空间；不使用额外数组。',
 '[1,2,3,4,5]，p=2 → [3,4,5,1,2]；p=7 同结果；p=0不变；空数组不取模。',
 '`[0,p-1]` 是要移到后面的前段；`[p,n-1]` 是要移到前面的后段。',
 ['n=0 时直接结束；否则先 p%=n，去掉整圈移动。','分别逆置前 p 个与后 n-p 个元素，使两段各自倒序。','再逆置整个数组：两段交换位置，段内次序同时恢复。'],
 '''
 void ReverseArray(int A[], int low, int high) {
     while (low < high) {
         int temp = A[low];
         A[low] = A[high];
         A[high] = temp;
         low++;
         high--;
     }
 }

 void LeftRotate(int A[], int n, int p) {
     if (n == 0) return;
     p = p % n;
     if (p == 0) return;
     ReverseArray(A, 0, p - 1);
     ReverseArray(A, p, n - 1);
     ReverseArray(A, 0, n - 1);
 }
 ''','O(n) / O(1)。','循环左移不是每次删除首项再插到末尾；后者重复 p 次可能是 O(np)。',
 '12345 左移2：前段逆置成21345，后段逆置成21543，整体逆置得到34512。')
card('A25','两个等长升序序列的中位数','主练','2011·42：训练定义为合并后第 n 小，即偶数总长度的较小中位数',
 'A、B 都是长度 n≥1 的非递减数组。求合并后第 n 小的元素，不实际合并，要求 O(log n) 时间、O(1) 辅助空间。',
 '[1,3,5] 与[2,4,6] → 3；[1]与[2] → 1；[1,1]与[1,2] → 1。',
 '`[low1,high1]`、`[low2,high2]` 是等长候选区间；同时舍去相同数量的较小元素与较大元素。',
 ['比较两段中点；相等时就是所求中位数。','若 A 的中点较小，舍弃 A 的一部分左端、B 的一部分右端；反之对称。','区间长度为奇数时保留两个中点；为偶数时，小中点所在区间要额外舍弃该中点，维持两段等长。','两段各剩一个数时，返回较小者。'],
 '''
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
 ''','O(log n) / O(1)。','不是两个中间数的平均值；奇偶判断看“当前候选区间长度”，不是一直看原 n。',
 'A=[1,3,5]，B=[2,4,6]：3<4，保留[3,5]与[2,4]；当前长2，3>2，保留[3]与[4]；较小者3。')
card('A26','数组主元素','主练','2013·41：不存在返回 -1',
 '找出长度 n≥0 的数组中出现次数严格大于 n/2 的主元素，不存在返回 -1，要求 O(n) 时间、O(1) 辅助空间。',
 '[2,1,2,2] → 2；[1,2,3] → -1；[1,1,2,2] → -1；[] → -1。',
 '`candidate` 为当前候选值；`count` 第一遍是抵消后的净票数，第二遍重新统计真实次数。',
 ['票数为0时，当前值成为新候选；相同值加票，不同值减票。','不同值两两抵消，不会把真正超过半数的值完全抵消。','但有候选不代表一定有主元素，必须第二遍验证。','真实次数>n/2 才返回候选，否则返回 -1。'],
 '''
 int Majority(const int A[], int n) {
     int candidate = 0;
     int count = 0;
     for (int i = 0; i < n; i++) {
         if (count == 0) {
             candidate = A[i];
             count = 1;
         } else if (A[i] == candidate) {
             count++;
         } else {
             count--;
         }
     }
     count = 0;
     for (int i = 0; i < n; i++) {
         if (A[i] == candidate) count++;
     }
     return count > n / 2 ? candidate : -1;
 }
 ''','O(n) / O(1)。','一定要验证，不是选出候选就直接返回；恰好一半不算主元素。若数组允许-1，返回值可能与失败码同值，这是本题接口约定。')
card('A27','三个升序数组的三元组最小距离','主练','2020·41：距离定义在本题明示，不与“三数之和/紧密三元组计数”混淆',
 '三个非递减非空整数数组 A、B、C，长度分别 n、m、t。各取一项 a、b、c，使 |a-b|+|b-c|+|c-a| 最小；返回该最小距离。',
 '[1,4,10]、[2,15,20]、[10,12] → 12（4,2,10或10,15,10）；[1]、[1]、[1] → 0；[-5]、[0]、[3] → 16。',
 '`i/j/k` 指向三数组当前元素；`minValue/maxValue` 为当前三元组极值。距离恒等于 2×(maxValue-minValue)。',
 ['从三个数组开头取当前三元组，更新最小距离。','若想缩小极差，推进当前最小值所在的数组；只推进非最小值不会改善当前最小值固定时的极差。','若最小值并列，可任选一个推进；若距离已为0，可直接结束。','任意一个数组耗尽后停止，不再有完整三元组。'],
 '''
 long long MinTripleDistance(const int A[], int n,
                             const int B[], int m,
                             const int C[], int t) {
     int i = 0, j = 0, k = 0;
     long long answer = LLONG_MAX;
     while (i < n && j < m && k < t) {
         int minValue = A[i];
         int maxValue = A[i];
         if (B[j] < minValue) minValue = B[j];
         if (C[k] < minValue) minValue = C[k];
         if (B[j] > maxValue) maxValue = B[j];
         if (C[k] > maxValue) maxValue = C[k];
         long long distance = 2 * ((long long)maxValue - minValue);
         if (distance < answer) answer = distance;
         if (answer == 0) break;
         if (A[i] == minValue) i++;
         else if (B[j] == minValue) j++;
         else k++;
     }
     return answer;
 }
 ''','O(n+m+t) / O(1)。','三个数组必须各取一个；不是在单数组找三数之和为0，也不是统计三元组数量。差值先转 long long 再减。',
 '当前(1,2,10)，距离18，推进最小值1；得到(4,2,10)，距离16；再推进2所在的B，继续扫描，最优在(10,15,10)，距离10。')
# Correct the worked example explicitly: (10, 15, 10) has distance 10, not 12.
cards['A27']['tests']='[1,4,10]、[2,15,20]、[10,12] → 10（10,15,10或10,15,12）；[1]、[1]、[1] → 0；[-5]、[0]、[3] → 16。'
card('L01','单链表原地逆置','基础积木','链表重排的前置操作；新版统一带头结点',
 '带头结点单链表 L，原地逆置数据结点；头结点地址不变，不新建数据结点。',
 'L→1→2→3 → L→3→2→1；空表、单结点均合法。',
 '`pre` 是已逆置部分的首结点；`p` 是当前待处理结点；`next` 暂存原后继。',
 ['pre 置空，p 从 L->next 开始，头结点不参加逆置。','先保存 p 原来的后继，再让 p 指向 pre。','pre 前进到 p，p 前进到原后继；直到原表扫描结束。','令 L->next=pre，把头结点接到逆置后的首结点。'],
 '''
 void ReverseList(LinkList L) {
     LNode *pre = NULL;
     LNode *p = L->next;
     while (p != NULL) {
         LNode *next = p->next;
         p->next = pre;
         pre = p;
         p = next;
     }
     L->next = pre;
 }
 ''','O(n) / O(1)。','改 p->next 之前必须保存原后继；不能把头结点当数据结点一起逆置。')
card('L02','稳定归并两个有序链表','基础积木','有序表操作；统一带头结点',
 'La、Lb 是两条带头结点的非递减单链表，不共享结点。复用全部数据结点归并到 La，相等时先取 La 原结点；保留 Lb 的头结点并使 Lb 成为空表。',
 'La=[1,3]、Lb=[1,2] → La=[1(a),1(b),2,3]、Lb=[]；两空表仍为空。',
 '`p/q` 指向两条待归并剩余链；`tail` 指向结果表最后一个结点。',
 ['先用 p、q 保存两条数据链，再把结果尾指针放在 La 头结点。','比较 p、q 的值，把较小结点尾插到结果；相等时先 p，保持稳定。','一条耗尽后，直接接上另一条剩余链。','清空 Lb->next，避免两个头结点继续指向同一批归并结果。'],
 '''
 void MergeLists(LinkList La, LinkList Lb) {
     LNode *p = La->next;
     LNode *q = Lb->next;
     LNode *tail = La;
     while (p != NULL && q != NULL) {
         if (p->data <= q->data) {
             tail->next = p;
             p = p->next;
         } else {
             tail->next = q;
             q = q->next;
         }
         tail = tail->next;
     }
     tail->next = (p != NULL) ? p : q;
     Lb->next = NULL;
 }
 ''','O(n+m) / O(1)。','本训练保留两个头结点；若原题要求释放 Lb 头结点，则按其所有权约定另行处理，不要擅自删除数据结点。')
card('L05','找前半段尾并断链','基础积木','链表重排的前置操作',
 '带头结点链表 L，至少2个数据结点。前半保留 ceil(n/2) 个，后半 floor(n/2) 个；断开两段，返回后半首结点。',
 '[1,2,3,4,5] → 前[1,2,3]、后[4,5]；[1,2] → [1]与[2]。',
 '`slow` 每次走一步；`fast` 每次走两步；退出时 slow 是前半段尾。',
 ['slow、fast 都从首个数据结点出发。','只要 fast 后面还有两个结点，两者分别前进1步、2步。','保存 slow->next 作为后半首，再令 slow->next=NULL 断链。'],
 '''
 LNode *SplitHalf(LinkList L) {
     LNode *slow = L->next;
     LNode *fast = L->next;
     while (fast->next != NULL && fast->next->next != NULL) {
         slow = slow->next;
         fast = fast->next->next;
     }
     LNode *second = slow->next;
     slow->next = NULL;
     return second;
 }
 ''','O(n) / O(1)。','本函数前提 n≥2；重排题在调用相同逻辑前，先处理空表/单结点。断链前先保存后半首。')
card('L07','首尾交替重排','主练','2019·41：按用户给出的题型改写',
 '带头结点链表 L 的数据结点为 a1→a2→…→an，改排为 a1→an→a2→an-1→…；不改变数据域，不新建数据结点，O(1) 辅助空间。',
 '[1,2,3,4,5] → [1,5,2,4,3]；[1,2,3,4] → [1,4,2,3]；空表不变。',
 '`slow` 找前半尾；`pre` 是逆置后的后半首；`p/q` 交替连接两段。',
 ['快慢指针找前半尾，奇数长度把中间结点留在前半。','保存后半首并断链，这一步防止后续重排成环。','把后半链就地逆置，得到 an→an-1→… 的顺序。','每次从后半取一个结点，插入当前前半结点后面，保存双方后继再改链。'],
 '''
 void ReorderList(LinkList L) {
     if (L->next == NULL || L->next->next == NULL) return;
     LNode *slow = L->next;
     LNode *fast = L->next;
     while (fast->next != NULL && fast->next->next != NULL) {
         slow = slow->next;
         fast = fast->next->next;
     }
     LNode *p = slow->next;
     slow->next = NULL;

     LNode *pre = NULL;
     while (p != NULL) {
         LNode *next = p->next;
         p->next = pre;
         pre = p;
         p = next;
     }

     p = L->next;
     LNode *q = pre;
     while (q != NULL) {
         LNode *next1 = p->next;
         LNode *next2 = q->next;
         p->next = q;
         q->next = next1;
         p = next1;
         q = next2;
     }
 }
 ''','O(n) / O(1)。','不是把所有结点压栈；断链和保存两个后继是最容易遗漏的地方。本卡已展开全部步骤，不依赖外部辅助函数。',
 '[1,2,3,4,5]：拆成123与45；后半逆为54；交替接成1→5→2→4→3。')
card('L09','两个链表的第一个公共结点','主练','2012·42：共同后缀首结点；按用户题型改写',
 '两条带头结点、无环的单链表 La、Lb 可能共享尾部，返回第一个公共数据结点地址；不存在返回 NULL。不修改、不释放结点。',
 '两条数据链长度5、3且共享最后2个结点 → 长链先走2步，再同步找到公共首；值相同但地址不同 → NULL。',
 '`length1/length2` 是数据结点数；`p/q` 对齐后到表尾的距离相同。',
 ['分别遍历两表统计长度，不把头结点计入。','较长表先走长度差步，让两个指针到表尾的距离相同。','同步后移，第一次地址相等就是公共后缀首；都到 NULL 表示无交点。'],
 '''
 LNode *FirstCommonNode(LinkList La, LinkList Lb) {
     int length1 = 0, length2 = 0;
     for (LNode *p = La->next; p != NULL; p = p->next) length1++;
     for (LNode *q = Lb->next; q != NULL; q = q->next) length2++;
     LNode *p = La->next;
     LNode *q = Lb->next;
     while (length1 > length2) {
         p = p->next;
         length1--;
     }
     while (length2 > length1) {
         q = q->next;
         length2--;
     }
     while (p != q) {
         p = p->next;
         q = q->next;
     }
     return p;
 }
 ''','O(n+m) / O(1)。','比的是 p==q，不是 p->data==q->data；本题有共享所有权，不能删除公共链上的结点。')
card('L14','链表倒数第 k 个结点','主练','2009·42：按用户题型改写，保留“成功输出并返回1、失败返回0”的形式',
 '带头结点链表 L，k 从1计数。只遍历一次，输出倒数第 k 个结点的数据并返回1；k≤0或表长不足 k 返回0，不输出。',
 '[1,2,3,4,5]，k=2 → 输出4，返回1；k=5 → 输出1；k=6或k=0 → 返回0；空表返回0。',
 '`p` 是先行指针，先走 k 步；`q` 从首个数据结点出发，之后与 p 同步。',
 ['若 k≤0，直接失败。','p 先走 k 步；没走够就遇到 NULL，说明结点不足。','q 从首结点出发，与 p 同步前进；p 到 NULL 时，q 恰为倒数第 k 个。','输出 q->data，返回成功标志1。'],
 '''
 int FindKthFromEnd(LinkList L, int k) {
     if (k <= 0) return 0;
     LNode *p = L->next;
     for (int i = 0; i < k; i++) {
         if (p == NULL) return 0;
         p = p->next;
     }
     LNode *q = L->next;
     while (p != NULL) {
         p = p->next;
         q = q->next;
     }
     printf("%d", q->data);
     return 1;
 }
 ''','O(n) / O(1)。','先行指针从数据首结点走 k 步、最后停在 NULL；不要与“先走 k-1 步、最后停在尾结点”的另一套循环混搭。')
card('L15','单链表按绝对值去重','主练','2015·41：利用题目给出的有限值域',
 '带头结点链表 L，所有数据满足 |data|≤maxValue，maxValue≥0。按原顺序只保留每个绝对值首次出现的结点，释放重复结点。所有结点由 new 单独创建且归本表所有。',
 '[21,-15,-15,-7,15]，maxValue=21 → [21,-15,-7]；[0,0] → [0]；[-3,3,-3] → [-3]。',
 '`visited[x]` 记录绝对值 x 是否已保留；`pre` 是 p 的前驱，删除后 pre 不移动。',
 ['申请 maxValue+1 个零标记，包含绝对值0。','读取 p 的绝对值；没见过就标记，并让 pre、p 后移。','已经见过则绕过 p 并 delete；p 回到 pre->next，pre 留在原处。','扫描结束后释放标记数组。'],
 '''
 void RemoveAbsDuplicates(LinkList L, int maxValue) {
     int *visited = new int[maxValue + 1]();
     LNode *pre = L;
     LNode *p = L->next;
     while (p != NULL) {
         int value = p->data < 0 ? -p->data : p->data;
         if (visited[value] == 0) {
             visited[value] = 1;
             pre = p;
             p = p->next;
         } else {
             pre->next = p->next;
             delete p;
             p = pre->next;
         }
     }
     delete[] visited;
 }
 ''','O(n+maxValue) / O(maxValue+1)，零初始化标记数组也有成本。','按绝对值去重，不是按原值；删除后不能再访问 p->next。值域前提排除了 INT_MIN 的取负溢出。')
card('T01','树高与平衡二叉树','基础积木','递归返回值',
 '空树高度0，叶结点高度1。先求树高，再判断任意结点的左右子树高差是否≤1；后者要求 O(n)。',
 '空树高度0且平衡；单结点高度1；连续3个左孩子形成的链不平衡。',
 '`leftHeight/rightHeight` 是两棵子树高度；平衡检查额外用 -1 表示这棵子树已经不平衡。',
 ['普通高度函数：空树返回0；非空返回左右高度较大值加1。','平衡判断用后序；任一子树返回-1，就把失败向上传递。','两个高度之差超过1也返回-1，否则返回当前真实高度。','最终返回值不是-1则整棵树平衡。'],
 '''
 int TreeHeight(BTNode *p) {
     if (p == NULL) return 0;
     int leftHeight = TreeHeight(p->lchild);
     int rightHeight = TreeHeight(p->rchild);
     return (leftHeight > rightHeight ? leftHeight : rightHeight) + 1;
 }

 int BalancedHeight(BTNode *p) {
     if (p == NULL) return 0;
     int leftHeight = BalancedHeight(p->lchild);
     if (leftHeight == -1) return -1;
     int rightHeight = BalancedHeight(p->rchild);
     if (rightHeight == -1) return -1;
     int difference = leftHeight - rightHeight;
     if (difference > 1 || difference < -1) return -1;
     return (leftHeight > rightHeight ? leftHeight : rightHeight) + 1;
 }

 bool IsBalanced(BTNode *root) {
     return BalancedHeight(root) != -1;
 }
 ''','两项分别为 O(n) / O(h)，h 为树高，退化树 h=n。','不要在每个结点重新遍历整棵子树求高度，否则最坏 O(n²)。')
card('T05','所有结点深度之和与带权路径长度','主练','2014·41：WPL；所有结点深度和仅用于对照概念',
 '二叉树根深度为0，叶结点 data 为权值。求 WPL=Σ(叶权×叶深度)；另写所有结点深度之和作区分。空树返回0。',
 '根带两个叶子，权2和3 → WPL=5；单结点 → 0；根的data无论多大，都不计入WPL。',
 '`depth` 是当前结点深度，沿递归参数向下传；返回值是当前子树的总贡献。',
 ['空结点贡献0。','叶结点贡献 data×depth，注意根若也是叶子，其深度仍为0。','非叶结点不贡献自己的权值，只返回左右子树贡献和；孩子深度加1。','对比 DepthSum：它是每个结点都贡献 depth，不是只有叶子。'],
 '''
 long long WPL(BTNode *p, int depth) {
     if (p == NULL) return 0;
     if (p->lchild == NULL && p->rchild == NULL) {
         return (long long)p->data * depth;
     }
     return WPL(p->lchild, depth + 1) + WPL(p->rchild, depth + 1);
 }

 long long DepthSum(BTNode *p, int depth) {
     if (p == NULL) return 0;
     return depth + DepthSum(p->lchild, depth + 1)
                  + DepthSum(p->rchild, depth + 1);
 }
 // 调用：WPL(root, 0)；DepthSum(root, 0)
 ''','O(n) / O(h)，递归栈计入辅助空间。','只有叶子参与 WPL；根从深度0开始。不要把“树高按层数从1算”套到路径长度。',
 '根下左叶2，右孩子下有叶3和4：WPL=2×1+3×2+4×2=16；右侧内部结点的data不参加求和。')
card('T07','递归先中后序遍历','基础积木','表达式树、WPL、BST 的递归积木',
 '分别输出二叉树先序、中序、后序，每个值后输出一个空格。',
 '根2、左1、右3：先序2 1 3；中序1 2 3；后序1 3 2；空树无输出。',
 '不额外维护全局状态；访问语句相对于“递归左、递归右”的位置决定遍历次序。',
 ['先判空；空树直接返回。','先序在递归前访问根；中序在左右递归之间访问根。','后序在左右递归都返回后访问根。'],
 '''
 void PreOrder(BTNode *p) {
     if (p == NULL) return;
     printf("%d ", p->data);
     PreOrder(p->lchild);
     PreOrder(p->rchild);
 }

 void InOrder(BTNode *p) {
     if (p == NULL) return;
     InOrder(p->lchild);
     printf("%d ", p->data);
     InOrder(p->rchild);
 }

 void PostOrder(BTNode *p) {
     if (p == NULL) return;
     PostOrder(p->lchild);
     PostOrder(p->rchild);
     printf("%d ", p->data);
 }
 ''','O(n) / O(h)。','中序输出不自动有序，只有满足 BST 条件时才有序。')
card('T16','表达式树转中缀表达式','主练','2017·41：按用户题型改写；用充分括号保留运算结构',
 '表达式树的叶子是单字符操作数，非叶是二元运算符且恰有两个孩子。输出等价中缀表达式：除整棵树的根表达式外，每个非叶子表达式都加一对括号；不要求最少括号。',
 '根*，左子树a+b，右叶c → (a+b)*c；根-，右子树b-c、左叶a → a-(b-c)；单叶a → a。',
 '`depth` 标识是否为整棵树的根：depth=0 的根不加最外层括号，其他非叶结点加。',
 ['中序输出是“左表达式、运算符、右表达式”，但只中序会丢失运算结合关系。','进入非根的非叶结点时，先输出左括号。','递归左子树，输出当前字符，再递归右子树。','离开同一个非叶结点时输出右括号；叶子不加括号。'],
 '''
 typedef struct ExprNode {
     char data;
     struct ExprNode *lchild, *rchild;
 } ExprNode;

 void PrintInfix(ExprNode *p, int depth) {
     if (p == NULL) return;
     bool needBrackets = depth > 0 && p->lchild != NULL;
     if (needBrackets) printf("(");
     PrintInfix(p->lchild, depth + 1);
     printf("%c", p->data);
     PrintInfix(p->rchild, depth + 1);
     if (needBrackets) printf(")");
 }

 void ExpressionToInfix(ExprNode *root) {
     PrintInfix(root, 0);
 }
 ''','O(n) / O(h)，输出长度也为 O(n)。','本题非叶恰有两个孩子，所以可用 lchild 判断非叶。不是看到乘除才加括号；减法、除法的右子树尤其不能随便省括号。',
 'a-(b-c)：根“-”不加最外层括号；右孩子也是“-”，进入时先输出“(”，中序输出b-c，退出时输出“)”。')
card('T17','顺序存储二叉树是否为 BST','主练','2022·41：按用户题型改写；训练的数组与空标记规则明确如下',
 '数组 A[0..n-1] 顺序存储一棵合法二叉树：根下标0，左右孩子2i+1、2i+2，-1为空；非空键均为非负整数，非空结点祖先必须非空。判断是否为严格 BST，不允许重复键。空树为真。',
 '[2,1,3] → 真；[10,5,15,-1,-1,6,20] → 假；[2,2,3] → 假；[-1]或[] → 真。',
 '`previous` 是中序中上一个访问的键；初值-1仅因本训练所有合法键≥0，不是适用于任意int的通用哨兵。',
 ['用下标递归代替指针递归，越界或空槽直接成功返回。','先检查左子树，再比较当前键与上一个中序键。','当前键必须严格更大；更新 previous 后检查右子树。','使用引用参数把同一份 previous 沿整次中序遍历共享；原题若用不同空标记，先按题意改接口。'],
 '''
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
 ''','O(n) 时间上界 / O(h) 递归栈；n是存储数组长度，若空槽很多不一定访问每个槽。','只比较父子不够：例中6虽是15的左孩子，却落在根10右子树中，仍然违法。不要把数组下标当键比较。孩子下标运算假定不溢出int。',
 '[10,5,15,-1,-1,6,20] 的非空中序为5,10,6,15,20；访问6时发现6≤10，立即判假。')
card('T18','BST 最近键值','主练','2026·41：仅依据用户提供的题型标题；下面是明示并列规则的训练版，不冒充原题全文',
 '给定严格 BST 与整数 target，返回键值和 target 的绝对差最小的结点；相同差时取较小键，空树返回 NULL。不改变树，要求 O(h) 时间、O(1) 辅助空间。',
 'BST键{2,4,6,8,10}，target=7 → 键6；target=9 → 键8；恰好命中直接返回；空树→NULL。',
 '`best` 为当前最优结点；`bestDifference` 为最小绝对差；`p` 沿普通 BST 查找路径前进。',
 ['空树直接返回 NULL，否则先用根作为候选。','每到一个结点计算绝对差，必要时更新最优候选；并列时按本训练取较小键。','target 小于当前键则走左；大于则走右；相等已经是最优，停止。','被舍弃一侧的键只会离 target 更远或不优于当前结点，所以不用遍历整棵树。'],
 '''
 BTNode *ClosestBST(BTNode *root, int target) {
     if (root == NULL) return NULL;
     BTNode *best = root;
     long long bestDifference = (long long)root->data - target;
     if (bestDifference < 0) bestDifference = -bestDifference;
     BTNode *p = root;
     while (p != NULL) {
         long long difference = (long long)p->data - target;
         if (difference < 0) difference = -difference;
         if (difference < bestDifference ||
             (difference == bestDifference && p->data < best->data)) {
             best = p;
             bestDifference = difference;
         }
         if (target == p->data) break;
         if (target < p->data) p = p->lchild;
         else p = p->rchild;
     }
     return best;
 }
 ''','O(h) / O(1)，平衡时 h=O(log n)，退化时可为 O(n)。','不能因为叫BST就无条件写 O(log n)；差值先转 long long。若真实原题的并列规则/返回形式不同，按原题调整，不能据标题断定一致。',
 '根8，左子树根4、其右孩子6，target=7：候选8差1；走到4不更优；走到6差1，依较小键规则把候选改为6。')
card('T19','BST 区间内键值递增输出','迁移选练','自编结构内迁移，不标真题年份；仅主练稳定后选做',
 '严格 BST，给定 low、high。把闭区间[low,high]中的键按递增顺序写入调用者提供的 result 数组并返回个数；容量足够，low>high时返回0。',
 '键{1,3,5,7,9}，区间[3,7] → [3,5,7]；[10,20] → []；空树→[]。',
 '`count` 是已写入个数；中序保证递增，BST大小关系用于剪掉不可能满足范围的子树。',
 ['当前键>low 才需要查左子树，否则左侧不可能落在区间内。','当前键在闭区间内就写入 result[count]，count++。','当前键<high 才需要查右子树；递归次序保持左、根、右。'],
 '''
 void CollectRange(BTNode *p, int low, int high, int result[], int &count) {
     if (p == NULL) return;
     if (p->data > low) CollectRange(p->lchild, low, high, result, count);
     if (p->data >= low && p->data <= high) {
         result[count] = p->data;
         count++;
     }
     if (p->data < high) CollectRange(p->rchild, low, high, result, count);
 }

 int BSTRange(BTNode *root, int low, int high, int result[]) {
     if (low > high) return 0;
     int count = 0;
     CollectRange(root, low, high, result, count);
     return count;
 }
 ''','O(h+k) / O(h)，k为输出数；退化时最坏 O(n)，输出数组另计。','这是“学过的BST＋范围条件”的小迁移，不是扩一套新算法；遍历顺序不可改成先根输出。')
card('S04','非递归中序遍历','基础积木','显式栈；服务树题，不单开栈队列冲刺主线',
 '二叉树结点数不超过 MAXSIZE，用显式栈中序输出到 result 数组并返回个数；输出数组容量足够，空树返回0。',
 '根2左1右3 → [1,2,3]；纯右链仍从根向下输出；空树→0。',
 '`top` 统一表示栈顶下标，空栈为-1；`p` 是当前要展开的子树；`count` 为输出个数。',
 ['p 非空时沿左链逐个入栈；入栈先++top再写。','左边走尽后弹出栈顶访问；弹栈先读再top--。','把 p 转向刚访问结点的右孩子，继续同样过程。','外层条件为 p 非空或栈非空，不能只判断 p。'],
 '''
 int IterInorder(BTNode *p, int result[]) {
     BTNode *stack[MAXSIZE];
     int top = -1;
     int count = 0;
     while (p != NULL || top != -1) {
         while (p != NULL) {
             stack[++top] = p;
             p = p->lchild;
         }
         p = stack[top--];
         result[count++] = p->data;
         p = p->rchild;
     }
     return count;
 }
 ''','O(n) / 本固定数组分配 O(MAXSIZE)，实际最多存 O(h) 个指针；若按已知高度动态申请才是 O(h) 分配空间。','top=-1 这套约定与旧版top表示个数不同，压栈/出栈/判空须一起改；固定数组不必为了统一初始化而改成 new。')
card('G07','拓扑序是否唯一','主练','2024·41：按用户题型改写',
 '有向图用公共约定的邻接表 ALGraph 存储。返回-1表示有环、无拓扑序；0表示拓扑序不唯一；1表示唯一。空图的空序列按唯一处理。',
 '0→1→2 → 1；0→2、1→2 → 0；0↔1 → -1；有独立点且另有环 → -1。',
 '`indegree[v]` 为剩余入度；`q[front..rear-1]` 为当前可选的零入度点；`count` 为已删除顶点数。',
 ['扫描所有边统计入度，把全部零入度点入队。','每次选点前，若队列里超过一个候选，则至少有两种选择，记住“不唯一”。','出队一个点，删除它的所有出边；相邻点入度减到0才入队。','必须处理到最后：count小于顶点数时先判有环；否则再根据此前候选数判唯一。'],
 '''
 int UniqueTopo(const ALGraph &G) {
     int n = G.vexnum;
     int *indegree = new int[n]();
     int *q = new int[n]();
     for (int v = 0; v < n; v++) {
         for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc) {
             indegree[p->adjvex]++;
         }
     }
     int front = 0, rear = 0;
     for (int v = 0; v < n; v++) {
         if (indegree[v] == 0) q[rear++] = v;
     }
     int count = 0;
     bool unique = true;
     while (front < rear) {
         if (rear - front > 1) unique = false;
         int v = q[front++];
         count++;
         for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc) {
             int w = p->adjvex;
             indegree[w]--;
             if (indegree[w] == 0) q[rear++] = w;
         }
     }
     delete[] indegree;
     delete[] q;
     if (count < n) return -1;
     return unique ? 1 : 0;
 }
 ''','O(V+E) / O(V) 辅助数组；图本身不计入额外空间。','发现多个零入度点时不要立刻返回0，剩余子图可能还有环；零入度选择必须逐轮检查，不是只看初始队列。',
 '0→2、1→2：初始队列有0、1两个候选，记不唯一；删完0和1后2入队，最终确实无环，才返回0。')
card('G13','有向图 K 顶点（出度大于入度）','主练','2023·41：按用户题型改写；用户已满分，安排间隔复写而非加量',
 '有向图邻接表 ALGraph，统计出度严格大于入度的顶点数。顶点编号0..vexnum-1。',
 '0→1、2→1 → 顶点0和2，共2个；空图0；只含一条自环的顶点入度=出度，不计。',
 '`outdegree[v]` 统计从 v 发出的邻接项；`indegree[w]` 统计所有指向 w 的邻接项。',
 ['申请两个长度为顶点数的零数组。','扫描 v 的每个邻接项 v→w，同时 outdegree[v]++、indegree[w]++。','扫描所有顶点，对严格 outdegree>indegree 的点计数。','释放两个辅助数组，返回计数。'],
 '''
 int CountKVertices(const ALGraph &G) {
     int n = G.vexnum;
     int *indegree = new int[n]();
     int *outdegree = new int[n]();
     for (int v = 0; v < n; v++) {
         for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc) {
             outdegree[v]++;
             indegree[p->adjvex]++;
         }
     }
     int count = 0;
     for (int v = 0; v < n; v++) {
         if (outdegree[v] > indegree[v]) count++;
     }
     delete[] indegree;
     delete[] outdegree;
     return count;
 }
 ''','O(V+E) / O(V)。','某顶点邻接表长度只能直接得到出度；求入度需要看全图所有邻接表。严格>，不是≥。')
card('G14','有向图两顶点间是否存在通路','迁移选练','自编结构内迁移；DFS/BFS 加目标条件，不标真题年份',
 '有向图邻接表 ALGraph，start、target 是合法顶点。判断从 start 到 target 是否存在通路，本训练允许长度为0的通路，因此 start==target 为真。',
 '0→1→2：0到2真，2到0假；不连通图中不可达为假；含环也必须结束。',
 '`visited[v]` 在入队时置1；`q` 存待扩展顶点，front/rear 均从0开始。',
 ['起点等于终点直接成功；否则起点入队并立刻标记。','逐个出队，检查它的所有出邻接点。','发现目标就记成功；其余未访问点入队并标记，避免环导致反复入队。','统一释放两个数组，再返回结果。'],
 '''
 bool HasPath(const ALGraph &G, int start, int target) {
     if (start == target) return true;
     int n = G.vexnum;
     int *visited = new int[n]();
     int *q = new int[n]();
     int front = 0, rear = 0;
     q[rear++] = start;
     visited[start] = 1;
     bool found = false;
     while (front < rear && !found) {
         int v = q[front++];
         for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc) {
             int w = p->adjvex;
             if (w == target) {
                 found = true;
                 break;
             }
             if (visited[w] == 0) {
                 visited[w] = 1;
                 q[rear++] = w;
             }
         }
     }
     delete[] visited;
     delete[] q;
     return found;
 }
 ''','最坏 O(V+E) / O(V)，零初始化数组本身也要 O(V)。','有向通路有方向；每个顶点最多入队一次的前提是入队时就标记，不是出队后才标记。')
card('H01','下滤与自底向上建堆','基础积木','堆排序/最小k个数的教材积木；冲刺主线的最小k个数在 A18',
 'A[0..n-1] 原地建大根堆，允许空数组。HeapAdjust 调用前，root 的左右子树已经分别成堆。全套默认0下标，因此孩子为2root+1、2root+2。',
 '[3,1,4,2] 建堆后满足父≥孩子；[]、[1]不变；不要求得到唯一的堆数组。',
 '`value` 暂存待下滤值；`child` 每次选择较大的孩子；`root` 是当前空位。',
 ['把当前根的值暂存，找到它较大的孩子。','暂存值已经≥较大孩子时，下滤结束。','否则把较大孩子上移到空位，空位下移，继续检查下一层。','从最后一个非叶结点 n/2-1 向前逐个下滤；叶子天然成堆。'],
 '''
 void HeapAdjust(int A[], int root, int n) {
     int value = A[root];
     int child = 2 * root + 1;
     while (child < n) {
         if (child + 1 < n && A[child + 1] > A[child]) child++;
         if (value >= A[child]) break;
         A[root] = A[child];
         root = child;
         child = 2 * root + 1;
     }
     A[root] = value;
 }

 void BuildMaxHeap(int A[], int n) {
     for (int i = n / 2 - 1; i >= 0; i--) {
         HeapAdjust(A, i, n);
     }
 }
 ''','一次下滤 O(log n)；自底向上建堆 O(n) / O(1)。','这是0下标版本，不要与教材1下标孩子2i、2i+1混用；建堆不等于已排好序。')

card('G15','无向连通图 EL 路径判定','主练','2021·41：用户记录14/15分，不是10分应用题，保留代码题主线',
 '无向连通简单图，用邻接表 ALGraph 存储，每条无向边存两个邻接项，顶点数至少1。判断能否从某点出发恰好经过每条边一次；允许起终点相同。单顶点无边按存在零长度欧拉通路处理。',
 '三角形：奇度点0个→真；一条链：奇度点2个→真；中心连3片叶的星形：奇度点4个→假。',
 '`degree` 是当前顶点的邻接表长度，即无向图的度；`oddCount` 是奇度顶点数。',
 ['题干已保证无向连通，不重复写DFS验证连通性。','逐顶点扫描邻接表，统计该点度数。','度为奇数就累加oddCount。','奇度点恰为0个或2个时存在所定义的通路，否则不存在。'],
 """
 bool HasELPath(const ALGraph &G) {
     int oddCount = 0;
     for (int v = 0; v < G.vexnum; v++) {
         int degree = 0;
         for (ArcNode *p = G.vertices[v].firstarc; p != NULL; p = p->nextarc) {
             degree++;
         }
         if (degree % 2 == 1) oddCount++;
     }
     return oddCount == 0 || oddCount == 2;
 }
 """,'O(V+E) / O(1)。','0个奇度点对应可闭合的欧拉回路，2个对应不同起终点的欧拉通路；本题允许两者。若题干未保证连通，必须另查所有有边顶点的连通性，不能只数奇度点。')

assert len(cards)==31,len(cards)
assert sum(c['level']=='主练' for c in cards.values())==19
assert sum(c['level']=='基础积木' for c in cards.values())==10
assert sum(c['level']=='迁移选练' for c in cards.values())==2

COMMON_CODE = '''#include <stdio.h>
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
} ALGraph;'''
COMMON = '''# 算法分类训练｜公共约定（408冲刺版）

[[算法分类训练-00总入口|← 总入口]] · [[算法分类训练-408真题对照与冲刺取舍|题目取舍与真题对照]]

> [!important] 这次真正统一什么
> 采用 **C++17 可编译、基础 C/C++ 教材风格**：普通数组、指针、结构体和必要的引用参数；不引入 STL、模板或哈希库。不是声称408只允许这一种语言。新版当前题卡代码不再与C11混用；留档中的旧C代码不是新版规范。

## 1. 数组申请与释放

```cpp
int *q = new int[n]();  // 申请 n 个 int，全部初始化为0
// 使用 q[0] 到 q[n-1]
delete[] q;            // 动态数组用 delete[]
```

- `new int[n]()` 是正确顺序，不是 `int new[n]`，也没有 `.`。`()` 表示值初始化，int元素初值为0。
- `new int[n]` 不保证整数元素是0，本套动态整数工作数组默认带 `()`。
- 零初始化只是初值；算法若要求 -1、无穷大等，仍需逐项赋值。
- 有固定上限时仍可 `int A[MAXSIZE];`，不强迫所有数组动态申请。未写先读不允许；无需读取的初始格不必清零。
- 单个结点 `new LNode{value, NULL}` 对应 `delete p`；动态数组对应 `delete[] p`。不混用 `malloc/free` 与 `new/delete`。
- 为突出算法，默认题目规模可分配、申请成功，数值与下标运算不溢出；不在每道冲刺题塞生产级异常处理。最小值域等题已明确额外限制。

## 2. 命名：能和题干直接对应

| 场景 | 统一含义 |
| --- | --- |
| `A`、`n`，`B`、`m` | 原数组与实际长度；不把容量当长度 |
| `i/j/k` | 下标，或题干已明确的第k个；局部说明具体职责 |
| `low/high/mid` | 二分或划分的左右闭区间与中点 |
| `q/front/rear` | 队列、下一出队位置、下一入队位置；空时front=rear |
| `stack/top` | 栈与栈顶下标；空栈top=-1，入栈stack[++top]，出栈stack[top--] |
| `p/q/pre/next` | 当前结点/另一指针/前驱/暂存后继；各题写明谁负责哪段链 |
| `visited` | 是否出现/访问，当前题内明确标记对象 |
| `indegree/outdegree` | 入度/出度，不再只写deg或rd让读者猜 |
| `leftMax/rightMin/suffixMax` | 左侧最大、右侧最小、后缀最大等题意状态 |
| `MAXSIZE` | 固定数组最大容量；实际规模另用n或vexnum |

保留熟悉的p、i等符号，不为了“短”把题意明确的变量缩成mn/mx/f/r。`const ALGraph &G` 表示只读引用，不复制整个图；`int &previous` 等表示递归中共享、可被更新的变量。

## 3. 公共类型（每道题只复制所需部分）

```cpp
''' + COMMON_CODE + '''
```

- **新版链表统一带头结点**：`L` 指向头结点，`L->next` 是第一个数据结点；头结点不算表长、不参加逆置。L本身非NULL，空表为L->next==NULL。
- 普通二叉树用data、lchild、rchild；空树为NULL，树高按层数（空0、叶1），路径深度按边数（根0）。表达式树因数据域为char，在题内单独定义ExprNode。
- 图采用邻接表ALGraph：vertices[v].firstarc 指向v的第一条出边；adjvex是邻接顶点下标，nextarc串接同一起点的邻接项。0≤vexnum≤MAXSIZE；图已合法构造，邻接点下标有效。
- 普通数组默认0下标。T17明确“-1为空、非空键非负”的训练输入格式；不要当作所有BST题都只能存非负键。
- 多数题只读写调用者的结果缓冲区，不在算法里新建输入数据结构；删除结点题要求这些结点由new创建并归当前链表所有。公共后缀题不释放共享结点。

## 4. 题解怎么读与编译

1. 题干先明确输入、输出、允许的操作与复杂度。
2. 展开题解先看“变量存什么”，再看编号步骤和小例子。
3. **每张当前题卡的cpp代码自含所需辅助函数**，只需公共类型/头文件，不用另找公共积木。不同题卡会重复Partition等函数；**每题单独编译，不要把整页题卡拼在同一个文件里。**
4. 编译：`g++ -std=c++17 -Wall -Wextra -Werror -pedantic -O2 exercise.cpp -o exercise`；main与造数/销毁代码属于测试，不必抄进考试答案。
5. 考场输出按“算法思想→核心代码→时间/空间”组织，空间要计递归栈、零初始化数组，不把结果缓冲区和工作空间混淆。

## 5. 状态与旧资料

- 19道真题题型主练、10个按需回补的基础积木、2道迁移选练；不是新增31道每日必做任务。
- 原72题编号、旧完成勾选均保留；接口/题解已变时，旧首次勾选只代表历史完成，是否会新版靠间隔复写核对，不自动宣称已掌握。
- 暂缓题仅保留定位、勾选和完整留档链接，不在冲刺页继续摆一份未统一的旧代码。
- 原版含个人批注/手写代码一并逐字节保留。留档不是正确性背书：例如旧A11题干是紧密三元组计数，代码却是无重复子数组长度，二者不符，不宜据旧答案学习。
- 验证范围见 [[算法分类训练-整理与校验记录]]，真题年份来源与未核实的接口差异见 [[算法分类训练-408真题对照与冲刺取舍]]。
'''

def qlink(qid, label=None):
 name=next(n for n in NAMES if n.split('-')[2][0]==qid[0])
 title=cards[qid]['title'] if qid in cards else sections[qid]['title']
 return '[['+name+'#'+qid+' '+title+'|'+(label or qid+' '+title)+']]'
def backup_link(name, heading=None):
 dest=(BACK.relative_to(P)/('原版-'+name+'.md')).as_posix()
 return '[['+dest+(('#'+heading) if heading else '')+'|改写前完整留档]]'

def render_card(c):
 qid=c['id']; oldcard=sections.get(qid)
 checks=oldcard['checks'] if oldcard else ['- [ ] 首次：能解释状态并写出代码','- [ ] 间隔复写：不看答案通过自测']
 body='### '+qid+' '+c['title']+'\n\n'+'\n'.join(checks)+'\n\n'
 body+='**定位**：'+c['level']+'｜'+c['source']+'。\n\n**题干**：'+c['prompt']+'\n\n**自测**：'+c['tests']+'\n\n'
 lines=['[!faq]- 题解与完整核心代码｜先说状态，再核对','**变量存什么**：'+c['states'],'','**解题步骤**']
 lines += [str(i+1)+'. '+step for i,step in enumerate(c['steps'])]
 if c['trace']: lines+=['','**手推一遍**：'+c['trace']]
 lines+=['','```cpp']+c['code'].splitlines()+['```','','**时间 / 额外空间**：'+c['cost'],'','**易错核对**：'+c['trap']]
 body+='\n'.join('> '+line if line else '>' for line in lines)+'\n\n'
 if oldcard:
  body+='旧作答/批注：'+backup_link(oldcard['file'],qid+' '+oldcard['title'])+'。\n\n'
 body+='**本题只记一处卡点**：____；下次先检查：____。\n\n'
 return body

def optional_reason(qid):
 if qid in ['A03','A04','A05','A07','A08','A09','A10','A11','A14','A15','A17','S02','S05','S06','G03','G06']:
  return '本轮不优先投入此类窗口/计数/刷题变式；它可以有训练价值，但与当前真题主线及剩余时间相比优先级降低。'
 if qid in ['A21','A22','A23']:
  return '后缀/历史极值的可选变式；先把A20的符号与更新时机写稳，不把每个变式都设为冲刺必刷。'
 if qid in ['G08','G09','G10','G11','G12']:
  return '保留教材算法复习价值，但不因原来题库有它就安排整套代码默写；选择/应用题另按章节复习。'
 if qid=='H03': return '本轮最小k个数主练归到A18；最大k个小根堆是可选的另一解法，不重复增加任务。'
 return '不是认定此题不会考；先完成真题型与必要积木，薄弱时再按需调用，不列入默认冲刺任务。'

outputs={}
for name in NAMES:
 letter=name.split('-')[2][0]
 topic={'A':'数组与线性表','L':'链表','T':'树与递归','S':'栈与队列','G':'图','H':'堆与排序'}[letter]
 cs=sorted([c for c in cards.values() if c['id'][0]==letter],key=lambda c:c['id'])
 text='# 408冲刺训练｜'+letter+' '+topic+'\n\n[[算法分类训练-00总入口|← 总入口]] · [[算法分类训练-公共约定|代码与类型约定]] · [[算法分类训练-408真题对照与冲刺取舍|真题对照与先后顺序]]\n\n'
 text+='> [!important] 不再从本页第一题一路清空\n> 只按“主练”路线前进；基础积木不会时再补，迁移题有余力再练。暂缓题原编号、勾选和完整留档保留，不构成新任务。旧首次完成记录沿用，能否写新版接口以间隔复写为准。\n\n'
 intros={
 'A':'本页主练是循环左移、等长中位数、主元素、标记桶、三数组最小距离、后缀极值及划分选择。窗口计数、三数之和等已退出默认主线。不是说数组题应当简单，而是先练题干限定范围内的扫描、标记、逆置和划分。',
 'L':'新版所有完整题卡统一**带头结点**。先抓先行指针、公共后缀、带前驱删除、拆分逆置重排四类；不再默认无头链表。需要释放的结点必须由new创建，使用delete。',
 'T':'优先“学过的树结构＋题目条件”：WPL、表达式树括号、顺序存储BST判断、BST查找路径。树高/遍历是积木；区间查询只是迁移选练，不是押题。',
 'S':'用户提供的2019·42循环单链表队列是10分应用题，不列代码题频次。本页只保留非递归中序作为树的按需积木；这不意味着栈队列的选择题、应用题不复习。',
 'G':'主练为入/出度扫描、EL路径判定与拓扑唯一性；通路存在性是遍历积木上的小迁移选练。最短路、生成树仍属教材内容，但不再把整套实现强塞进代码题冲刺。',
 'H':'用户题单中的“集合均分”与“最小k个数”用划分选择串起来：'+qlink('A19')+'、'+qlink('A18')+'。本页建堆只作为教材积木，别与A专题重复加任务。'}
 text+=intros[letter]+'\n\n## 本专题路线\n\n| 层级 | 题目 |\n| --- | --- |\n'
 for level in ['主练','基础积木','迁移选练']:
  for c in cs:
   if c['level']==level: text+='| '+level+' | [[#'+c['id']+' '+c['title']+'|'+c['id']+' '+c['title']+']] |\n'
 if not cs: text+='| 暂缓 | 原题见下方留档入口 |\n'
 text+='\n每张当前题卡的cpp代码可独立配公共类型编译，**不要拼整页**；辅助函数已在各卡展开。\n\n'
 for level,head in [('主练','主练：真题题型'),('基础积木','基础积木：卡住再补'),('迁移选练','迁移选练：有余力再做')]:
  group=[c for c in cs if c['level']==level]
  if group:
   text+='## '+head+'\n\n'
   for c in group: text+=render_card(c)
 remaining=[(q,s) for q,s in sections.items() if q[0]==letter and q not in cards]
 if remaining:
  text+='## 暂缓题：只保留定位与历史记录\n\n'
  for q,s in remaining:
   text+='### '+q+' '+s['title']+'\n\n'+'\n'.join(s['checks'])+'\n\n**本轮定位**：暂缓。'+optional_reason(q)+'\n\n'
   if q=='A11': text+='> [!warning] 旧答案与题干不符\n> 原题问紧密三元组计数，旧代码却求最长无重复段。留档只保存历史，不将这段代码当答案。本轮对应真题的三数组最小距离改练 '+qlink('A27')+'。\n\n'
   text+='完整原题、旧代码、个人批注及卡点：'+backup_link(name,q+' '+s['title'])+'。\n\n'
 # Keep every original h2/h3 anchor, including subcategory entry points used by existing notes.
 current_heads=set(re.findall(r'^#{1,6} (.+)$',text,re.M))
 missing=[h for h in old_heads[name] if h not in current_heads]
 if missing:
  text+='## 旧分组与附记入口（兼容原链接）\n\n'
  raw=old[name+'.md']
  for h in missing:
   level='### ' if re.search(r'^### '+re.escape(h)+r'$',raw,re.M) else '## '
   text+=level+h+'\n\n'
   if h in ['本专题公共积木']:
    text+='新版每张题卡已展开所需辅助函数，无须额外拼接一份公共积木。\n\n'
   else:
    matched=re.search(r'^#{2,3} '+re.escape(h)+r'\n(.*?)(?=^## |\Z)',raw,re.M|re.S)
    ids=re.findall(r'^### ([ALTHSG]\d{2}) ',matched.group(1),re.M) if matched else []
    text+=('本旧分组定位：'+' · '.join(qlink(q) for q in ids)+'。' if ids else '历史附记见 '+backup_link(name,h)+'；本轮不额外增加任务。')+'\n\n'
 outputs[name+'.md']=text
outputs['算法分类训练-公共约定.md']=COMMON
(WORK/'cards.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2),encoding='utf-8')
(WORK/'common.hpp').write_text(COMMON_CODE+'\n',encoding='utf-8')
MAPPING = [
 ('2009·42','链表倒数第K个结点','8/15','L14','L'),
 ('2010·42','数组循环左移','9/13','A24','A'),
 ('2011·42','两个等长升序序列的中位数','12/15','A25','A'),
 ('2012·42','单链表共同后缀首结点','11/13','L09','L'),
 ('2013·41','数组主元素','12/13','A26','A'),
 ('2014·41','二叉树WPL','5/13','T05','T'),
 ('2015·41','单链表按绝对值去重','13/15','L15','L'),
 ('2016·43','集合均分最大化和差','10/15','A19','排序'),
 ('2017·41','表达式树转中缀表达式','2/15','T16','T'),
 ('2018·41','未出现的最小正整数','12/13','A12','A'),
 ('2019·41','重排链表','10/13','L07','L'),
 ('2020·41','三个升序数组的三元组最小距离','5/13','A27','A'),
 ('2021·41','无向连通图EL路径判定','14/15','G15','G'),
 ('2022·41','顺序存储二叉树是否为BST','9/13','T17','T'),
 ('2022·42','数组最小K个数','未提供','A18','排序'),
 ('2023·41','有向图K顶点：出度>入度','13/13','G13','G'),
 ('2024·41','拓扑排序是否唯一','9/13','G07','G'),
 ('2025·41','后缀最大乘积数组','11/13','A20','A'),
 ('2026·41','BST最近键值','5/13','T18','T'),
]
assert len(MAPPING)==19
assert {r[3] for r in MAPPING}=={q for q,c in cards.items() if c['level']=='主练'}
FIRST=['T16','T05','A27','T18','L14','G07']
SECOND=['A24','A25','A26','A12','A20','A18','A19','L09','L15','L07','T17','G13','G15']
assert set(FIRST+SECOND)=={r[3] for r in MAPPING}
STRATEGY='''# 408真题对照与冲刺取舍（2026-11-05）

[[算法分类训练-00总入口|← 总入口]] · [[算法分类训练-公共约定|新版代码规范]]

> [!important] 本次结论
> 不把原72题全部刷完作为目标，改为 **19道真题题型主练＋10个按需基础积木＋2道迁移选练**。新增题是补原套题的真题型缺口，不是给冲刺再扩一套题库。原题不物理删除，54道原编号题退出默认主线，并保留完整历史记录。

## 1. 来源和边界：不把题型标题当原题全文

- 年份、题号、题型、个人得分均来自KK在2026-11-05这次消息中提供的题单，**不是另行核实过的历年试卷全文**。本次未获得可用的官方全文/考试日程核验结果，不据此杜撰原题细节或官方日期。
- 仅排除两道10分应用题：2019·42可复用空间的循环单链表队列（4/10）、2020·42前缀编码译码（2/10）。这是本轮代码训练的排除，不是整个408复习都跳过它们。
- **2021·41 EL路径判定的记录是14/15，不属于10分应用题，保留。** 2022·42没有提供个人得分，不自行补全。
- 当前题卡是“对应题型的训练版”，输入、输出、空值标记、并列规则都在题干写明；不冒充原题原文。做原卷时仍以原卷为准。
- 特别待对照原题的细节：2025后缀最大乘积是否允许自身；2026最近键值并列如何处理；2022顺序存储树的根下标/空标记。当前分别明示训练约定，不在代码里偷偷假设。
- 冲刺节奏按用户给出的**2026年12月20日**节点倒排；从2026年11月5日相隔45天。这个节点用于本地训练安排，不作为已核实的官方考试日程声明。

## 2. 逐年题型与训练卡对应

| 用户提供的题号 | 题型 | 用户记录 | 当前训练卡 |
| --- | --- | --- | --- |
'''
for year,title,score,qid,cat in MAPPING:
 STRATEGY+='| '+year+' | '+title+' | '+score+' | '+qlink(qid)+' |\n'
STRATEGY+='''
## 3. 频次能说明什么，不能说明什么

仅按这份给定清单、排除两道10分应用题后统计：

| 领域 | 代码题数量 | 训练上的含义 |
| --- | --- | --- |
| 数组扫描/逆置/有序性/标记/极值 | 6 | 数组不能整体降权，应该换掉偏刷题的题目结构 |
| 单链表 | 4 | 指针距离、共同后缀、删除、拆分重排可作为一组积木练 |
| 树与BST | 4 | 递归参数/返回值、中序、查找路径，比泛化树题数量更重要 |
| 图 | 3 | 先练邻接表扫描、度数和拓扑过程，不先背四套最短路/MST实现 |
| 排序/划分选择 | 2 | 第k小、最小k个、均分极值可以用一次Partition串联 |

- 这是**所给题单内的计数**，不是考试大纲权重或各模板的出题概率；数组与划分在知识上也有交叉，分类只是为安排训练。
- 不能从“上次考树，所以这次轮到链表”推导概率，也不能说图连续出现就更可能/更不可能再出现。
- 本轮给树题更多投入，主要因为表达式树2/15、WPL5/13、BST最近键值5/13暴露了明确的个人缺口，不是预测下一次更容易考树。
- 三数组最小距离5/13也要前置：它依旧是有序性＋多指针推进，不需要为了去力扣化把这种真正相关的线性扫描一起删掉。
- 已得13/13的K顶点、14/15的EL路径只做间隔复写与边界核对；不因为列为主练就再投入同样时间。

## 4. 为什么旧数组训练显得偏力扣

优先下调：三数之和、各种窗口长度/计数、无重复段、前缀状态计数、旋转数组最小值、单调栈循环变式。这不是断言它们绝不会考，而是它们在当前套题里占比偏高，挤掉了已经出现过的循环左移、主元素、等长中位数等基本题型。

保留为主线：题干给出数据结构/有序性/值域，要求组织扫描、标记、划分或结构操作，并明确时间/空间。**408风格不等于题目简单，也不等于所有力扣题都不相关；关键是覆盖与投入是否匹配。**

旧A11还存在题干与代码不一致：题干问紧密三元组计数，代码却求最长无重复段。本次不把它“换个变量名”继续当答案，而是退出主线、保留历史，并单独补真正的三数组最小距离A27。

## 5. 真正执行的两轮路线

### 第一轮：6道优先补洞

'''
for i,qid in enumerate(FIRST,1):
 STRATEGY+=str(i)+'. '+qlink(qid)+'。\n'
STRATEGY+='''
这6道里先补个人低分的4道，再用链表先行指针、拓扑过程做不同结构切换。卡在某个基础积木时，只补对应积木，不重启一整个专题。

### 第二轮：13道真题型补齐与保温

'''
for i,qid in enumerate(SECOND,1): STRATEGY+=str(i)+'. '+qlink(qid)+'。\n'
STRATEGY+='''
A18与A19连着练，L07卡住再补L01/L05；T17卡住补T07。G13/G15接近满分，一次闭卷通过就进入间隔复写，不给自己安排机械重刷。

### 有余力才做的两道迁移

'''+qlink('T19')+'、'+qlink('G14')+'。它们只是“原结构＋新条件”的有限迁移，不标成预测题。\n\n'+'''
## 6. 按时间安排，不把代码练习挤成全天任务

| 时间 | 任务 | 停止条件 |
| --- | --- | --- |
| 11月5日—11月15日 | 优先6道，边做边补所需积木 | 看完可说清状态、遮住能写；下一次先复写其中一道 |
| 11月16日—11月30日 | 其余13道，已有高分题只检验 | 不按专题从头扫；一题过关就换结构 |
| 12月1日—12月13日 | 从19道中混合限时输出，少量结构内迁移 | 连续写出思路、代码、复杂度，重点记录失败步骤 |
| 12月14日—12月19日 | 只回收仍会写错的卡点、接口和边界 | 不再临时扩窗口/哈希/堆变式的新题单 |

- 一次30—45分钟；困难题可拆成两次，不要求每日两题，不挤占其他科目。限时输出可先以每题20—25分钟试运行，再按实际总卷节奏调整。
- 第一次展开答案是学习，不伪装闭卷；随后遮住代码重写才算练输出。
- 最小完成单元：一句算法思想＋完整核心函数及必要辅助函数＋复杂度＋至少正常/最小/易错三类自测。
- 原72题的历史勾选不撤销，也不自动计作新版通过。旧作答留档可回看，但不要再次用未校正的旧代码作为新版答案。
'''
outputs['算法分类训练-408真题对照与冲刺取舍.md']=STRATEGY

ENTRY='''# 算法分类训练｜408冲刺：真题型优先，基础按需补

> [!important] 当前主线（2026-11-05调整）
> 不再要求清空原72题。现在按 **19道真题题型主练＋10个按需基础积木＋2道迁移选练** 训练。数组已减少窗口/计数类刷题变式；链表、树、图围绕已学结构组织算法。旧编号、完成勾选和个人批注保留，54道旧题退出默认主线而不是抹掉历史。

详细取舍、逐年对应、个人薄弱点与时间安排：[[算法分类训练-408真题对照与冲刺取舍]]。

## 1. 下一次直接从这里开始

**先做 '''+qlink('T16')+'''。** 这是你给出的2/15分题型；先把“中序遍历为什么还不够、括号加在什么结点”理解并写出。递归顺序还不熟才回补 '''+qlink('T07')+'''，不必先清完整个数组专题。

第一轮顺序：

'''
for i,qid in enumerate(FIRST,1): ENTRY+=str(i)+'. '+qlink(qid)+'\n'
ENTRY+='''
第二轮13道和两道迁移按 [[算法分类训练-408真题对照与冲刺取舍#5. 真正执行的两轮路线|两轮路线]] 继续；不是猜今年必考什么。

## 2. 专题入口与分层

| 专题 | 真题型主练 | 按需积木 | 迁移选练 | 入口 |
| --- | --- | --- | --- | --- |
'''
for name in NAMES:
 letter=name.split('-')[2][0]
 levels=[sum(c['id'][0]==letter and c['level']==lev for c in cards.values()) for lev in ['主练','基础积木','迁移选练']]
 ENTRY+='| '+letter+' | '+' | '.join(map(str,levels))+' | [['+name+']] |\n'
ENTRY+='''| 合计 | **19** | **10** | **2** | 基础与迁移不是额外必刷题单 |

- 19道与用户题单逐一对应；仅排除两道10分应用题。2021 EL路径记录为14/15，保留；2022最小k个数未提供得分，不补猜。
- 数组页承接了划分选择的两道排序真题型，所以H页没有另算主练，避免重复。
- 当前31张完整题卡统一为基础C++、常用变量名、状态说明、编号步骤、题内自测；不是声称31张都要从零开始刷。
- 暂缓题的原题干/旧代码/个人批注在每题的“改写前完整留档”中；旧代码不等于新版规范或已校正答案。

## 3. 每次怎么练

1. 读题先说清输入、输出、允许修改什么、目标复杂度。
2. 不会时展开FAQ，先看“变量存什么”和小例子，再看代码。
3. 遮住答案，从函数签名开始写；所需辅助函数已在当前题卡展开，不用到处找。
4. 用正常、最小、易错三类例子检查，再核对边界和复杂度。
5. 下次先复写上次卡住的那题；能写后才进入下一题，不用把整个专题当关卡。

一次30—45分钟，难题允许拆两次。旧首次勾选沿用，只代表历史完成；是否会新版以间隔复写核对，不自动替你勾选。

## 4. 代码约定先统一，不再临时问AI翻译

完整说明和公共类型见 [[算法分类训练-公共约定]]。

- 动态整数数组：`int *q = new int[n]();`，用完`delete[] q;`；固定容量数组可保留`MAXSIZE`。
- 链表统一带头结点L，首个数据结点L->next；单结点申请与释放用new/delete。
- 队列front/rear，栈top=-1表示空；二分用low/high/mid的闭区间版本。
- 图用教材式ALGraph、ArcNode、firstarc、adjvex、nextarc；入度/出度直接命名indegree/outdegree。
- 每张当前题卡独立配公共类型编译；不要拼接整页中重复的Partition等辅助函数。

## 5. 与旧材料怎样共存

| 材料 | 当前用途 |
| --- | --- |
| 本套六专题＋真题对照 | 当前冲刺主线与按需回补 |
| [[2.知识库/20.North_star_ZJU/202.计算机知识/05数据结构/08算法题/03算法题模板|03算法题模板]] | 历史识别信号与分类参考；本次未重写，代码口径以新版公共约定与当前题卡为准 |
| [[2.知识库/20.North_star_ZJU/202.计算机知识/05数据结构/08算法题/04 二叉树模板|04 二叉树模板]]、[[2.知识库/20.North_star_ZJU/202.计算机知识/05数据结构/08算法题/堆|堆]] | 对应章节查阅，不另加一套冲刺任务 |
| [[算法分类训练-旧题覆盖索引]] | 历史题型定位；找到题不代表本轮都要刷 |
| 原四周混合训练、30天计划、旧题单 | 保留原记录，只按需要抽题，不再并行清空 |

原四周入口：[[训练第1周-混合保温]]（已完成记录保留）· [[训练第2周-混合保温]] · [[训练第3周-混合保温]] · [[训练第4周-混合保温]]。

改写前完整留档见各题链接；实际编译、测试、勾选与链接核对范围见 [[算法分类训练-整理与校验记录]]。

## 6. 卡点记录仍然保持短

> 卡在：读题约束／变量含义／推进条件／递归参数或返回／断链释放／边界。下次先检查：____。

不要把看过答案与独立写出混为一次完成。冲刺不是继续堆题量，而是把这些题型变成能自己写出的结构操作。
'''
outputs['算法分类训练-00总入口.md']=ENTRY
INDEX_NAME='算法分类训练-旧题覆盖索引.md'
idx=old[INDEX_NAME]
pos=idx.find('\n')
idx=idx[:pos+1]+'''\n> [!important] 2026-11-05冲刺口径
> 此表只保留历史题型定位，不代表仍须清空全部旧题。当前按 [[算法分类训练-408真题对照与冲刺取舍]] 的19道主练前进；旧标题锚点仍在，暂缓题可跳到逐字节留档。历史分类/纠错说明不替代新版题干与代码。
\n'''+idx[pos+1:]
idx=idx.replace('#A11 紧密三元组计数\\|','#A11 紧密三元组计数- 好题\\|')
outputs[INDEX_NAME]=idx
AUDIT_NAME='算法分类训练-整理与校验记录.md'
auditold=old[AUDIT_NAME]
pos=auditold.find('\n')
newaudit='''

## 2026-11-05：408冲刺重编（本次）

- 口径：用户提供的21条历年题目记录中，仅排除两道10分应用题；2021·41 EL路径是14/15，仍属主练。共19道真题题型、10个按需积木、2道自编迁移选练。
- 旧72题保留编号与两项勾选，新增13个缺口/迁移题号；54道旧题退出默认主线，仅留定位与完整历史链接。数字85是兼容旧编号后的题卡总数，不是新的必刷量。
- 完整代码统一为基础C++17；动态整数数组new int[n]()、数组delete[]、单结点delete；链表改带头结点；栈top=-1；二分闭区间；图使用教材式邻接表字段。每卡自含辅助函数，按卡独立编译，不拼整页。
- 题解统一“变量职责→编号步骤→必要手推→代码→复杂度→易错”。A16针对选中文段改写；A11旧题干/代码不符，明确警示、不沿用旧代码。
- 年份/得分来自用户题单；真实试卷全文与考试日程未获可用官方核验结果，不声称核实。2025自身范围、2026并列规则、2022空值标记等均明示训练约定。
- 原10份“算法分类训练”笔记逐字节复制到“算法分类训练-改写前留档-2026-11-05”，文件名前加“原版-”避免短名冲突。未改旧计划、四周训练、待刷笔记、父目录模板或其他笔记，未扫描全库。
- 校验工作文件放在当前练习题目录的隐藏子目录`.408-code-check-2026-11-05`，包含生成脚本、逐卡提取代码、测试与哈希清单，不污染复习入口。

### 本次最终验证结果

待执行编译、运行与链接/历史记录审计；这里不会沿用下方2026-10-24的C11测试作为本次通过证明。

---

> [!note] 以下保留旧记录
> 下方2026-10-24记录仅针对当时的旧版本；其C11“整页拼接编译”方法不适用于本次每卡独立的C++版本。改写前原始记录已另行留档。
'''
outputs[AUDIT_NAME]=auditold[:pos+1]+newaudit+'\n'+auditold[pos+1:]

# Do not overwrite data edited after our snapshot.
for name, digest in manifest.items():
 assert hashlib.sha256((P/name).read_bytes()).hexdigest()==digest, '检测到并发编辑：'+name
for name,text in outputs.items():
 for invisible in ['\u200b','\u200c','\u200d']: text=text.replace(invisible,'')
 text=''.join(re.sub(r'\[\[[^\]]+\]\]',lambda m:re.sub(r'(?<!\\)\|',r'\\|',m.group()),line) if line.startswith('|') else line for line in text.splitlines(keepends=True))
 assert '\ufffd' not in text,name
 assert '????' not in text,name
 (P/name).write_text(text,encoding='utf-8')
(WORK/'mapping.json').write_text(json.dumps(MAPPING,ensure_ascii=False,indent=2),encoding='utf-8')
print('Written:',len(outputs),'notes;',len(cards),'complete cards; 19 main + 10 foundation + 2 transfer.')
print('Original numbered cards:',len(sections),'; originals kept:',len(originals))
print('Backup verification:',all(hashlib.sha256((BACK/('原版-'+n)).read_bytes()).hexdigest()==h for n,h in manifest.items()))
