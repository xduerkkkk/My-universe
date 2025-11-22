# 1143.最长公共子序列

[力扣题目链接(opens new window)](https://leetcode.cn/problems/longest-common-subsequence/)

给定两个字符串 text1 和 text2，返回这两个字符串的最长公共子序列的长度。

一个字符串的 子序列 是指这样一个新的字符串：它是由原字符串在不改变字符的相对顺序的情况下删除某些字符（也可以不删除任何字符）后组成的新字符串。

例如，"ace" 是 "abcde" 的子序列，但 "aec" 不是 "abcde" 的子序列。两个字符串的「公共子序列」是这两个字符串所共同拥有的子序列。

若这两个字符串没有公共子序列，则返回 0。

示例 1:

- 输入：text1 = "abcde", text2 = "ace"
- 输出：3
- 解释：最长公共子序列是 "ace"，它的长度为 3。
## 题解

```python
   def longestCommonSubsequence(self, text1: str, text2: str) -> int:

        dp = [[0]*(len(text2)+1) for _ in range(len(text1)+1)]

  

        for i in range(1,len(text1)+1):

            for j in range(1,len(text2)+1):

                if text1[i-1] == text2[j-1]:

                    dp[i][j] = dp[i-1][j-1] + 1

                else:

                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        return dp[len(text1)][len(text2)]

```
核心困惑点应在于：如果 text1[i-1] 和 text2[j-1] 不相等，则当前位置的最长公共子序列长度为上方或左方的较大值
**当前字符不可用**，要继承更优的子问题解（不破坏相对顺序）
# 53. 最大子序和

[力扣题目链接(opens new window)](https://leetcode.cn/problems/maximum-subarray/)

给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

示例:

- 输入: [-2,1,-3,4,-1,2,1,-5,4]
- 输出: 6
- 解释: 连续子数组 [4,-1,2,1] 的和最大，为 6。
## 题解
之前学贪心的时候做过？
记录count即可，如果大于ans就更新ans
如果小于ans，那我们就另找个连续数组之头，把count记为0，重新来过

```python
 def maxSubArray(self, nums: List[int]) -> int:

        count = 0

        ans = -inf

  

        for i in range(len(nums)):

            count += nums[i]

            if count >ans:

                ans = count

            if count <= 0:

                count = 0

        return ans

```

训练动态规划哈
也一样，这个记录ans其实就蕴含到每一个dp里面

```培养、thon
 def maxSubArray(self, nums: List[int]) -> int:

        dp = [0]*len(nums)

        dp[0] = nums[0]

        ans = dp[0]

  

        for i in range(1,len(nums)):

            dp[i] = max(dp[i-1]+nums[i], nums[i])

            ans = max(ans,dp[i])

        return ans
```
# 392.判断子序列

[力扣题目链接(opens new window)](https://leetcode.cn/problems/is-subsequence/)

给定字符串 s 和 t ，判断 s 是否为 t 的子序列。

字符串的一个子序列是原始字符串删除一些（也可以不删除）字符而不改变剩余字符相对位置形成的新字符串。（例如，"ace"是"abcde"的一个子序列，而"aec"不是）。

示例 1：

- 输入：s = "abc", t = "ahbgdc"
- 输出：true

示例 2：

- 输入：s = "axc", t = "ahbgdc"
- 输出：false
## 题解
与最长公共子序列是一样的。
核心就是判断这个t和s的最长公共子序列的长度，是不是s的长度。
