# 455分饼干

## 题解
就单从直觉上讲哈
最小的饼干给需求最少的孩子
是最合理的分配，没问题吧
我们也可以反证，最小的饼干没给胃口最小的孩子，给了第二小的孩子。那胃口最小的孩子将拿到的是比较大的饼干，不就浪费资源了吗
```python
class Solution:
    def findContentChildren(self, g, s):
        g.sort()  # 将孩子的贪心因子排序
        s.sort()  # 将饼干的尺寸排序
        index = 0
        for i in range(len(s)):  # 遍历饼干
            if index < len(g) and g[index] <= s[i]:  # 如果没遍历完孩子，且当前孩子能吃这个饼干
                index += 1  # 满足一个孩子，指向下一个孩子
        return index  # 返回满足的孩子数目
```
# 376 摆动序列
如果连续数字之间的差严格地在正数和负数之间交替，则数字序列称为摆动序列。第一个差（如果存在的话）可能是正数或负数。少于两个元素的序列也是摆动序列。

例如， [1,7,4,9,2,5] 是一个摆动序列，因为差值 (6,-3,5,-7,3)  是正负交替出现的。相反, [1,4,7,2,5]  和  [1,7,4,5,5] 不是摆动序列，第一个序列是因为它的前两个差值都是正数，第二个序列是因为它的最后一个差值为零。

给定一个整数序列，返回作为摆动序列的最长子序列的长度。 通过从原始序列中删除一些（也可以不删除）元素来获得子序列，剩下的元素保持其原始顺序。
## 题解
把题目转变成形象一点的：所谓摆动序列不过是找山峰与山谷的个数（局部最优）
只不过，只有一个数，或者两个不同数，也视作为山峰山谷。
为了满足题目的这个要求，我们只能初始化
result = 1  
```python
class Solution:
    def wiggleMaxLength(self, nums):
        if len(nums) <= 1:
            return len(nums)  # 如果数组长度为0或1，则返回数组长度
        curDiff = 0  # 当前一对元素的差值
        preDiff = 0  # 前一对元素的差值
        result = 1  # 记录峰值的个数，初始为1
        for i in range(len(nums) - 1):
            curDiff = nums[i + 1] - nums[i]  # 计算下一个元素与当前元素的差值
            # 如果遇到一个峰值
            if (preDiff <= 0 and curDiff > 0) or (preDiff >= 0 and curDiff < 0):
                result += 1  # 峰值个数加1
                preDiff = curDiff  # 注意这里，只在摆动变化的时候更新preDiff
        return result  # 返回最长摆动子序列的长度
```

# 最长子序列
给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
## 题解
贪心在哪呢？
注意哈，强调一下，连续子数组
如果全是正数，123423
肯定全要了
但就是出现负数，让我们不能全要
**输入：nums = [-2,1,-3,4,-1,2,1,-5,4]**
**输出：6**
**解释：连续子数组 [4,-1,2,1] 的和最大，为 6 。**

那我们怎么找连续子数组？
从头开始不断累加，碰到负数就不要它？
不行
万一是 20 -1 20呢？ 本来能3个一起要39的，如果把-1丢掉就只能20了
如果碰到累加和为负数，就不要它了
1 1 -3 10 20
从1开始加，加到-3发现，累加和给我干到-1了， 那我们本次count（即累加和）的计算就停了，找下一组吧（10 20 等着我们呢） 

```python
class Solution:

    def maxSubArray(self, nums: List[int]) -> int:

        count = 0

        ans = -inf

  

        for i in range(len(nums)):

            count += nums[i]

            if count < 0:

                count = 0

            else:

                ans = max(count,ans)

        return ans

```
这是有问题的，并不是count >= 0 就更新ans，那如果 -1 -2 -3 咋办？ 这个逻辑的话ans永远无法更新

换了下，还是有问题

```python
class Solution:

    def maxSubArray(self, nums: List[int]) -> int:

        count = 0

        ans = -inf

  

        for i in range(len(nums)):

            count += nums[i]

            if count <= 0:

                count = 0

            if count >ans:

                ans = count

        return ans

```

问题在哪？哈哈，问题在顺序上，我们不能更新了count再让有可能改变了的count与ans比较，


这次没问题

```python
 for i in range(len(nums)):

            count += nums[i]

            if count >ans:

                ans = count

            if count <= 0:

                count = 0

```
