本part，沿用上一part
- **如果求组合数就是外层for循环遍历物品，内层for遍历背包**。
- **如果求排列数就是外层for遍历背包，内层for循环遍历物品**
的思想


那思考下面的题要考虑遍历顺序吗？

如何设计才能不考虑？
# 322 零钱兑换
给定不同面额的硬币 coins 和一个总金额 amount。编写一个函数来计算可以凑成总金额所需的最少的硬币个数。如果没有任何一种硬币组合能组成总金额，返回 -1。

你可以认为每种硬币的数量是无限的。

示例 1：

- 输入：coins = [1, 2, 5], amount = 11
- 输出：3
- 解释：11 = 5 + 5 + 1
## 题解

```python
 def coinChange(self, coins: List[int], amount: int) -> int:

        dp = [float('inf')]*(amount+1)

        dp[0] = 0

  

        for coin in coins:

            for i in range(coin,amount+1):

                dp[i] = min(dp[i],dp[i-coin]+1)

        if dp[amount] == float('inf'):  # 如果最终背包容量的最小硬币数量仍为正无穷大，表示无解

            return -1

        return dp[amount]
```



# 279 完全平方数
给你一个整数 `n` ，返回 _和为 `n` 的完全平方数的最少数量_ 。

**完全平方数** 是一个整数，其值等于另一个整数的平方；换句话说，其值等于一个整数自乘的积。例如，`1`、`4`、`9` 和 `16` 都是完全平方数，而 `3` 和 `11` 不是。

**示例 1：**

**输入：**n = `12`
**输出：**3 
**解释：**`12 = 4 + 4 + 4`

## 题解

```python
def numSquares(self, n: int) -> int:

        dp = [float('inf')] * (n + 1)

        dp[0] = 0

  

        for i in range(1, int(n ** 0.5) + 1):  # 遍历物品

            for j in range(i * i, n + 1):  # 遍历背包

                # 更新凑成数字 j 所需的最少完全平方数数量

                dp[j] = min(dp[j - i * i] + 1, dp[j])

  

        return dp[n]
```
# 139 单词拆分
给定一个非空字符串 s 和一个包含非空单词的列表 wordDict，判定 s 是否可以被空格拆分为一个或多个在字典中出现的单词。

说明：

拆分时可以重复使用字典中的单词。

你可以假设字典中没有重复的单词。

示例 1：

- 输入: s = "leetcode", wordDict = ["leet", "code"]
- 输出: true
- 解释: 返回 true 因为 "leetcode" 可以被拆分成 "leet code"。

示例 2：

- 输入: s = "applepenapple", wordDict = ["apple", "pen"]
- 输出: true
- 解释: 返回 true 因为 "applepenapple" 可以被拆分成 "apple pen apple"。
- 注意你可以重复使用字典中的单词。
## 题解
tips：这个是很显然的求组合
```python
dp = [False]*(len(s) + 1)
        dp[0] = True
        # 遍历背包
        for j in range(1, len(s) + 1):
            # 遍历单词
            for word in wordDict:
                if j >= len(word):
                    dp[j] = dp[j] or (dp[j - len(word)] and word == s[j - len(word):j])
        return dp[len(s)]
```