# 121 买卖股票
给定一个数组 prices ，它的第 i 个元素 prices[i] 表示一支给定股票第 i 天的价格。

你只能选择 某一天 买入这只股票，并选择在 未来的某一个不同的日子 卖出该股票。设计一个算法来计算你所能获取的最大利润。

返回你可以从这笔交易中获取的最大利润。如果你不能获取任何利润，返回 0 。

- 示例 1：
    
- 输入：[7,1,5,3,6,4]
    
- 输出：5  
    解释：在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格；同时，你不能在买入前卖出股票。

## 题解
可以直接选靠左边的最小值，靠右边的最大值
或者不断更新最小的price，维护` 当前price - 最小price` 即可
```python
  n = len(prices)
    if n == 0: 
        return 0
    min_price = prices[0]
    max_profit = 0
    for i in range(1, n):
        min_price = min(min_price, prices[i])          # 维护历史最低价
        max_profit = max(max_profit, prices[i] - min_price) # 更新当前最大利润
    return max_profit
```
不过为了训练动态规划我们还是想想dp数组怎么写
一维行不行？其实不能直观用一维定义，和打家劫舍不同，“抢还是不抢”一维就能蕴含这个信息。而本题，股票是**多状态决策问题**，需同时记录“是否持有股票”与“历史交易行为”，是不是两个状态呢？打家劫舍只有一个状态。
以示例输入 `[7,1,5,3,6,4]` 演示：

|天数|prices|dp[i][0]|dp[i][1]|
|---|---|---|---|
|0|7|-7|0|
|1|1|max(-7, -1) = -1|max(0, -7+1)=0|
|2|5|max(-1, -5) = -1|max(0, -1+5)=4|
|3|3|max(-1, -3) = -1|max(4, -1+3)=4|
|4|6|max(-1, -6) = -1|max(4, -1+6)=5|
|5|4|max(-1, -4) = -1|max(5, -1+4)=5|

持有状态，有可能今天才持的，收益：`-prices[i]` ，有可能之前持 收益：`dp[i-1][0]` 
不持有状态，有可能今天不持有的（卖股票）收益：`dp[i-1][0] + prices[i]` ，有可能之前就是不持有，收益：`dp[i-1][1]`

最终

```python
def maxProfit(self, prices: List[int]) -> int:

        n = len(prices)
  
        dp=[[0]*2 for _ in range(n)]
        dp[0][0] = -prices[0]

        for i in range(1,n):
            dp[i][0] = max(dp[i-1][0],-prices[i])
            dp[i][1] = max(dp[i-1][1], dp[i-1][0] + prices[i])

        return dp[-1][1]

```
# 122 买卖股票的最佳时机 II
给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。

设计一个算法来计算你所能获取的最大利润。你可以尽可能地完成更多的交易（多次买卖一支股票）。

注意：你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。

- 示例 1:
    
- 输入: [7,1,5,3,6,4]
    
- 输出: 7  
    解释: 在第 2 天（股票价格 = 1）的时候买入，在第 3 天（股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5-1 = 4。随后，在第 4 天（股票价格 = 3）的时候买入，在第 5 天（股票价格 = 6）的时候卖出, 这笔交易所能获得利润 = 6-3 = 3 。

## 题解 

非动态规划

```python
def maxProfit(self, prices: List[int]) -> int:

        ans = 0

        for i in range(len(prices)-1):

            m = prices[i+1] - prices[i]

            ans += max(m,0)

        return ans
```
使用动态规划

```python
 def maxProfit(self, prices: List[int]) -> int:

        length = len(prices)

        dp = [[0] * 2 for _ in range(length)]

        dp[0][0] = -prices[0]

        dp[0][1] = 0

        for i in range(1, length):

            dp[i][0] = max(dp[i-1][0], dp[i-1][1] - prices[i]) #注意这里是和121. 买卖股票的最佳时机唯一不同的地方

            dp[i][1] = max(dp[i-1][1], dp[i-1][0] + prices[i])

        return dp[-1][1]

```
本题是可以多次卖卖股票，与第一题的区别仅仅为
`  dp[i][0] = max(dp[i-1][0], dp[i-1][1] - prices[i])` 

# 123 [买卖股票的最佳时机 III](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iii/)
给定一个数组，它的第 i 个元素是一支给定的股票在第 i 天的价格。

设计一个算法来计算你所能获取的最大利润。你最多可以完成 两笔 交易。

注意：你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。

- 示例 1:
    
- 输入：prices = [3,3,5,0,0,3,1,4]
    
- 输出：6 解释：在第 4 天（股票价格 = 0）的时候买入，在第 6 天（股票价格 = 3）的时候卖出，这笔交易所能获得利润 = 3-0 = 3 。随后，在第 7 天（股票价格 = 1）的时候买入，在第 8 天 （股票价格 = 4）的时候卖出，这笔交易所能获得利润 = 4-1 = 3。
    
- 示例 2：
    
- 输入：prices = [1,2,3,4,5]
    
- 输出：4 解释：在第 1 天（股票价格 = 1）的时候买入，在第 5 天 （股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5-1 = 4。注意你不能在第 1 天和第 2 天接连购买股票，之后再将它们卖出。因为这样属于同时参与了多笔交易，你必须在再次购买前出售掉之前的股票。
```python
  if len(prices) == 0:
            return 0
        dp = [[0] * 5 for _ in range(len(prices))]
        dp[0][1] = -prices[0]
        dp[0][3] = -prices[0]
        for i in range(1, len(prices)):

            dp[i][1] = max(dp[i-1][1],  - prices[i])
            dp[i][2] = max(dp[i-1][2], dp[i-1][1] + prices[i])
            dp[i][3] = max(dp[i-1][3], dp[i-1][2] - prices[i])
            dp[i][4] = max(dp[i-1][4], dp[i-1][3] + prices[i])
        return dp[-1][4]
```