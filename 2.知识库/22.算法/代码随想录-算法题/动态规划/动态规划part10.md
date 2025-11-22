# 300.最长递增子序列

[力扣题目链接(opens new window)](https://leetcode.cn/problems/longest-increasing-subsequence/)

给你一个整数数组 nums ，找到其中最长严格递增子序列的长度。

子序列是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，[3,6,2,7] 是数组 [0,3,1,6,2,2,7] 的子序列。

示例 1：

- 输入：nums = [10,9,2,5,3,7,101,18]
- 输出：4
- 解释：最长递增子序列是 [2,3,7,101]，因此长度为 4 。

示例 2：

- 输入：nums = [0,1,0,3,2,3]
- 输出：4
## 题解

```python
def lengthOfLIS(self, nums: List[int]) -> int:

        n = len(nums)

        dp = [1]*n

  

        for i in range(1,n):

            for j in range(0,i):

                if nums[i] > nums[j]:

                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)

```
# 674. 最长连续递增序列

[力扣题目链接(opens new window)](https://leetcode.cn/problems/longest-continuous-increasing-subsequence/)

给定一个未经排序的整数数组，找到最长且 连续递增的子序列，并返回该序列的长度。

连续递增的子序列 可以由两个下标 l 和 r（l < r）确定，如果对于每个 l <= i < r，都有 nums[i] < nums[i + 1] ，那么子序列 [nums[l], nums[l + 1], ..., nums[r - 1], nums[r]] 就是连续递增子序列。

示例 1：

- 输入：nums = [1,3,5,4,7]
- 输出：3
- 解释：最长连续递增序列是 [1,3,5], 长度为3。尽管 [1,3,5,7] 也是升序的子序列, 但它不是连续的，因为 5 和 7 在原数组里被 4 隔开。

示例 2：

- 输入：nums = [2,2,2,2,2]
- 输出：1
- 解释：最长连续递增序列是 [2], 长度为1。
## 题解

```python
 def findLengthOfLCIS(self, nums: List[int]) -> int:

        n = len(nums)

        dp = [1]*n

  

        for i in range(1,n):

            if nums[i] > nums[i-1] :

                dp[i] = dp[i-1] + 1

  

        return max(dp)
```

# 718. 最长重复子数组

[力扣题目链接(opens new window)](https://leetcode.cn/problems/maximum-length-of-repeated-subarray/)

给两个整数数组 A 和 B ，返回两个数组中公共的、长度最长的子数组的长度。

示例：

输入：

- A: [1,2,3,2,1]
- B: [3,2,1,4,7]
- 输出：3
- 解释：长度最长的公共子数组是 [3, 2, 1] 。


```python
def findLength(self, nums1: List[int], nums2: List[int]) -> int:

        result = 0

        dp = [[0]*(len(nums2)+1) for _ in range(len(nums1)+1)]

  

        for i in range(1,len(nums1)+1):

            for j in range(1,len(nums2)+1):

                if nums1[i-1] == nums2[j-1]:

                    dp[i][j] = dp[i-1][j-1] + 1

                if dp[i][j] > result:

                    result = dp[i][j]

  

        return result

```
