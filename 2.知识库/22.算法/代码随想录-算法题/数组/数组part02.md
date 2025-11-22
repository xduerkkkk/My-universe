
# 长度最小的子数组
### 题目描述
给定一个含有 `n` 个正整数的数组和一个正整数 `target` **。**

找出该数组中满足其总和大于等于 `target` 的长度最小的 **子数组** `[numsl, numsl+1, ..., numsr-1, numsr]` ，并返回其长度**。**如果不存在符合条件的子数组，返回 `0` 。

**示例 1：**

**输入：**target = 7, nums = [2,3,1,2,4,3]
**输出：**2
**解释：**子数组 `[4,3]` 是该条件下的长度最小的子数组。

下面是错误演示，没有优化，ans初始化错误 
（思考一下，如何优化ans？ans应如何初始化？）

```python
class Solution:

    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        l, r = 0, 0
        sum = 0
        ans = 0
        lenth = len(nums)
        while r < lenth:
            sum += nums[r]
            while sum >= target:
                ans = (r - l + 1)
                sum -= nums[l]
                l += 1
            r += 1

        return 0 if ans == 0 else ans

```


快慢指针其实会遍历每一个数。快指针走，走到满足>=target的地方，开始等慢指针，
ans不能是0，0也是有效答案。我们要不断优化ans，是不断取最小，于是初始化ans要大（大于lenth就可以）
正确解法：
```python
 def minSubArrayLen(self, target: int, nums: List[int]) -> int:

        l, r = 0, 0

        sum = 0

        lenth = len(nums)

        ans = inf

        while r < lenth :

            sum += nums[r]

            while sum >= target:

                ans = min(ans, r - l + 1)

                sum -= nums[l]

                l += 1

            r += 1

  

        return 0 if ans == inf else ans
```
904水果成蓝，哈希表＋滑动窗口
# 59.螺旋矩阵II

纯粹的模拟法：
```python
class Solution:

    def generateMatrix(self, n: int) -> List[List[int]]:

        ans_matrix = [[0]*n for _ in range(n)]
        loops = n//2  # 要“右，下，左，上”这样的循环几次？ 数学验证一下是n//2
        x = y = 0
        count = 1 #待填入的数

  
        for loop in range(1, loops + 1):#分别处理右、下、左、上

            for i in range(y, n - loop): # 注意没有走到头，右边是开区间！下面都是

                ans_matrix[x][i] = count

                count += 1

            for i in range(x, n - loop):

                ans_matrix[i][n-loop] = count

                count += 1

            for i in range(n - loop, y, -1):

                ans_matrix[n - loop][i] = count

                count += 1

            for i in range(n-loop, x, -1):

                ans_matrix[i][y] = count

                count += 1

            x += 1
            y += 1
            
# 如果是奇数矩阵，还少填一个中间的空
        mid = n//2
        
        if n%2 != 0:
            ans_matrix[mid][mid] = count

        return ans_matrix
```
机器人法！ 定义DIRS，即机器人的步伐。这里忘贴，可以思考一下如何定义
对于一个机器人，它要判断的就是边界是什么，即外界环境变成什么样了，就开始改变策略
当然是出界！ `di = (di + 1) % 4  # 右转 90°` 这里比较巧妙地表达了若出界，则调转方向的逻辑
x, y 是下一步！ 不是当前，x，y是机器人试探时，走的预想位置
```python
    def generateMatrix(self, n: int) -> List[List[int]]:
        ans = [[0] * n for _ in range(n)]
        i = j = di = 0
        for val in range(1, n * n + 1):  # 要填入的数
            ans[i][j] = val
            x, y = i + DIRS[di][0], j + DIRS[di][1]  # 下一步的位置
            # 如果 (x, y) 出界或者已经填入数字
            if x < 0 or x >= n or y < 0 or y >= n or ans[x][y]:
                di = (di + 1) % 4  # 右转 90°
            i += DIRS[di][0]
            j += DIRS[di][1]  # 走一步
        return ans


```
# 区间和

###### 题目描述

给定一个整数数组 Array，请计算该数组在每个指定区间内元素的总和。

###### 输入描述

第一行输入为整数数组 Array 的长度 n，接下来 n 行，每行一个整数，表示数组的元素。随后的输入为需要计算总和的区间下标：a，b （b > = a），直至文件结束。

###### 输出描述

输出每个指定区间内元素的总和。


区间长度，用前缀和解决，这可以说是一个可以记住的技巧！
下面有两个运行时间天差地别的方案，区别在于输入！
所以acm格式一定要注意如何输入速度更快

```python
def main():

    n = int(input())
    array = [int(input()) for _ in range(n)]
    prefix = [0]*(n+1)

    for i in range(n):
        prefix[i+1] = prefix[i] + array[i]

    while True:
        try:
            a, b = map(int, input().split())
            print(prefix[b+1]-prefix[a])
        except EOFError:

            break
```
运行时间9000ms

```python
import sys

def main():
    data = list(map(int, sys.stdin.read().split()))
    
    n = data[0]
    array = data[1:n+1]
    queries = data[n+1:]

    # 构建前缀和
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + array[i]

    # 处理查询
    results = []
    for i in range(0, len(queries), 2):
        a = queries[i]
        b = queries[i + 1]
        results.append(str(prefix[b + 1] - prefix[a]))

    print('\n'.join(results))
```
运行时间300ms

# 开发商购买土地（第五期模拟笔试）

###### 题目描述

[44. 开发商购买土地（第五期模拟笔试）](https://kamacoder.com/problempage.php?pid=1044)

既然提到了总和，仍然是“前缀和”方法！
注意这里偏记忆性的矩阵前缀和构造方式：`prefix[i+1][j+1] = matrix[i][j] + prefix[i+1][j] + prefix[i][j+1] -prefix[i][j]`

```python
def main():
	n, m = map(int, input().split())
	matrix = [list(map(int, input().split())) for _ in range(n)]

	prefix = [[0]*(m+1) for _ in range(n+1)]
	for i in range(n):
		for j in range(m):
		prefix[i+1][j+1] = matrix[i][j] + prefix[i+1][j] + prefix[i][j+1] -prefix[i][j]
			
	total = prefix[n][m]
    min_diff = float('inf')

    # 横向划分（按行分割）
    for i in range(1, n):
        top = prefix[i][m]
        bottom = total - top
        min_diff = min(min_diff, abs(top - bottom))

    # 纵向划分（按列分割）
    for j in range(1, m):
        left = prefix[n][j]
        right = total - left
        min_diff = min(min_diff, abs(left - right))
    
    print(min_diff)

```

