# 1049 最后一块石头的重量
有一堆石头，每块石头的重量都是正整数。

每一回合，从中选出任意两块石头，然后将它们一起粉碎。假设石头的重量分别为 x 和 y，且 x <= y。那么粉碎的可能结果如下：

如果 x == y，那么两块石头都会被完全粉碎；

如果 x != y，那么重量为 x 的石头将会完全粉碎，而重量为 y 的石头新重量为 y-x。

最后，最多只会剩下一块石头。返回此石头最小的可能重量。如果没有石头剩下，就返回 0。

示例：

- 输入：[2,7,4,1,8,1]
- 输出：1

解释：

- 组合 2 和 4，得到 2，所以数组转化为 [2,7,1,8,1]，
- 组合 7 和 8，得到 1，所以数组转化为 [2,1,1,1]，
- 组合 2 和 1，得到 1，所以数组转化为 [1,1,1]，
- 组合 1 和 1，得到 0，所以数组转化为 [1]，这就是最优值。
## 题解

考的仍然是个转换思维
```python
  def lastStoneWeightII(self, stones: List[int]) -> int:

        target = sum(stones) // 2

        dp = [0]*(target+1)

  

        for stone in stones:

            for j in range(target, stone-1, -1):

                dp[j] = max(dp[j], dp[j-stone]+stone)

  

        return (sum(stones) - dp[-1]*2 )
```


- 设总重量为 `total = sum(stones)`。
- 分组后两组的重量分别为 `group1` 和 `group2`，满足：
    
    
    `group1 + group2 = total group1 <= total // 2  # 因为背包容量是 total//2`
    
- 最小差值为：
    
    `min_diff = (total - group1) - group1 = total - 2*group1`
    
- 由于 `dp[-1]` 是 `group1` 的最大可能值（即 `max(group1)`），因此：
    
    `min_diff = total - 2*dp[-1]`
# 474 一和零
给你一个二进制字符串数组 strs 和两个整数 m 和 n 。

请你找出并返回 strs 的最大子集的大小，该子集中 最多 有 m 个 0 和 n 个 1 。

如果 x 的所有元素也是 y 的元素，集合 x 是集合 y 的 子集 。

示例 1：

- 输入：strs = ["10", "0001", "111001", "1", "0"], m = 5, n = 3
    
- 输出：4
    
- 解释：最多有 5 个 0 和 3 个 1 的最大子集是 {"10","0001","1","0"} ，因此答案是 4 。 其他满足题意但较小的子集包括 {"0001","1"} 和 {"10","1","0"} 。{"111001"} 不满足题意，因为它含 4 个 1 ，大于 n 的值 3 。
## 题解
这题是一维的dp数组，
但是二维的数据！
所以写出来是`dp[i]dp[j]`。

既然是一维的dp数组，要注意逆序遍历

```python
 dp = [[0] * (n + 1) for _ in range(m + 1)]  # 创建二维动态规划数组，初始化为0
        # 遍历物品
        for s in strs:
            ones = s.count('1')  # 统计字符串中1的个数
            zeros = s.count('0')  # 统计字符串中0的个数
            # 遍历背包容量且从后向前遍历
            for i in range(m, zeros - 1, -1):
                for j in range(n, ones - 1, -1):
                    dp[i][j] = max(dp[i][j], dp[i - zeros][j - ones] + 1)  # 状态转移方程
        return dp[m][n]
```


