由于part01比较简单，所以和part02放在一起
part01的题，斐波那契函数、爬楼梯，都是引入动态规划的思想
即每个状态，都是由相邻两个状态递推而来的。我们可以一步一步递推，把每一个状态都推出了

其中，还要注意范围
比如爬楼梯我第一次写了一个错误代码

```python
dp = [0]*(n+1)

        dp[1] = 1

        dp[2] = 2

        for i in range(3,n+1):

            dp[i] = dp[i-1] +dp[i-2]

        return dp[n]
```
题目说，输入的n>=1  那如果n=1，初始化的dp【2】不就index out of range了？ 
所以我们先看看题目输入的范围，如果输入的最小值是初始化的值，那输入最小值是我们直接返回那个初始化值即可
即
```python
 if n <= 1:
            return n
```
# 746 使用最小花费爬楼梯
数组的每个下标作为一个阶梯，第 i 个阶梯对应着一个非负数的体力花费值 cost[i]（下标从 0 开始）。

每当你爬上一个阶梯你都要花费对应的体力值，一旦支付了相应的体力值，你就可以选择向上爬一个阶梯或者爬两个阶梯。

请你找出达到楼层顶部的最低花费。在开始时，你可以选择从下标为 0 或 1 的元素作为初始阶梯。

**示例 1：**

输入：cost = [10,_15_,20]
**输出：15
解释：你将从下标为 1 的台阶开始。
- 支付 15 ，向上爬两个台阶，到达楼梯顶部。
总花费为 15 。

示例 2：
**输入：cost = [_**1**_,100,_**1**_,1,_**1**_,100,_**1**_,_**1**_,100,_**1**_]
**输出：6
解释：你将从下标为 0 的台阶开始。
- 支付 1 ，向上爬两个台阶，到达下标为 2 的台阶。
- 支付 1 ，向上爬两个台阶，到达下标为 4 的台阶。
- 支付 1 ，向上爬两个台阶，到达下标为 6 的台阶。
- 支付 1 ，向上爬一个台阶，到达下标为 7 的台阶。
- 支付 1 ，向上爬两个台阶，到达下标为 9 的台阶。
- 支付 1 ，向上爬一个台阶，到达楼梯顶部。
总花费为 6 
## 题解
注意看示例1，我把三个台阶标出来了，哎，理解题意也很重要啊。所以从二号台阶（下标为1）再向上爬两个才到楼梯顶部
![[动态规划part01，part02-1750479491252.jpeg]]
也就是，如果长度为3的cost，我们最后要算出4个dp，我们要的是第四个的dp，也就是dp【3】
有点绕，数组初始化，range，数组下标都要搞清楚
之前两题中，dp【0】我们是不用的，废弃的。
但本题为了和cost下标节奏相同，我们把dp【0】也用了起来
那既然用了dp【0】为什么还初始化n+1个，就是因为dp个数要比cost.lenth多一个！ （从上图中可以看到)。所以我们最后循环时，算的最后一个数也是dp【n】，dp【n】是n+1个dp！
```python
def minCostClimbingStairs(self, cost: List[int]) -> int:

        n = len(cost)

        dp = [0]*(n+1)

  

        for i in range(2,n+1):

            dp[i] = min(dp[i-1]+cost[i-1],dp[i-2]+cost[i-2])

  

        return dp[n]
```
# 62.不同路径
一个机器人位于一个 `m x n` 网格的左上角 （起始点在下图中标记为 “Start” ）。

机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为 “Finish” ）。

问总共有多少条不同的路径？
## 题解
注意 [[初始化数组]]

```python
 def uniquePaths(self, m: int, n: int) -> int:

        dp=[[0]*n for _ in range(m)]

  

        for i in  range(m):

            dp[i][0] = 1

        for i in range(n):

            dp[0][i] = 1

  

        for i in range(1, m):

            for j in range(1, n):

                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

        return dp[m - 1][n - 1]
```
# 63 不同路径II
一个机器人位于一个 m x n 网格的左上角 （起始点在下图中标记为“Start” ）。

机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为“Finish”）。

现在考虑网格中有障碍物。那么从左上角到右下角将会有多少条不同的路径？
- 输入：obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
- 输出：2 解释：
- 3x3 网格的正中间有一个障碍物。
- 从左上角到右下角一共有 2 条不同的路径：
    1. 向右 -> 向右 -> 向下 -> 向下
    2. 向下 -> 向下 -> 向右 -> 向右
## 题解
首先给出错解

```python
 def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:

        m = len(obstacleGrid)

        n = len(obstacleGrid[0])

  

        if obstacleGrid[m - 1][n - 1] == 1 or obstacleGrid[0][0] == 1:

            # 如果起点或终点有障碍物，直接返回0

            return 0

  

        dp = [[0]*n for _ in range(m)]

        for i in range(n):

            if obstacleGrid[0][i] != 1:

                dp[0][i] = 1

        for i in range(m):

            if obstacleGrid[i][0] != 1:

                dp[i][0] = 1

        for i in range(1,m):

            for j in range(1,n):

                if obstacleGrid[i][j] != 1:

                    dp[i][j] = dp[i-1][j]+dp[i][j-1]

  

        return dp[m-1][n-1]
```
其错误之处在于，初始化第一行和第一列。如果有障碍，不应该跳过，而是后方全部置为0.脑海没有模拟检查！
所以注意正确的初始化：

```python
for i in range(n):

            if obstacleGrid[0][i] == 1:

                break

            dp[0][i] = 1

        for i in range(m):

            if obstacleGrid[i][0] == 1:

                break

            dp[i][0] = 1
```
