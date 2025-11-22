# 739. 每日温度

[力扣题目链接(opens new window)](https://leetcode.cn/problems/daily-temperatures/)

请根据每日 气温 列表，重新生成一个列表。对应位置的输出为：要想观测到更高的气温，至少需要等待的天数。如果气温在这之后都不会升高，请在该位置用 0 来代替。

例如，给定一个列表 temperatures = [73, 74, 75, 71, 69, 72, 76, 73]，你的输出应该是 [1, 1, 4, 2, 1, 1, 0, 0]。

提示：气温 列表长度的范围是 [1, 30000]。每个气温的值的均为华氏度，都是在 [30, 100] 范围内的整数。
## 题解
单调栈
每次索引都要进栈的，但是进栈前都要看看，“如果我进去，栈顶的元素是最小这个状态，有没有被我打破“。如果打破了，我得把这些都清扫出去，我必须要有一席之地呀。所以是while循环。
因为每个索引都要挨个进栈的（for i in range（n）） 所以，元素看是谁踢走的它，就能确定最近的，比他大的元素是哪个索引
`answer[stack[-1]] = i - stack[-1]`
```python
  def dailyTemperatures(self, temperatures: List[int]) -> List[int]:

        n = len(temperatures)

        stack = []

        answer = [0]*n

  

        for i in range(n):

            while stack and temperatures[i] > temperatures[stack[-1]]:

                answer[stack[-1]] = i - stack[-1]

                stack.pop()

            stack.append(i)

  
	    return answer```


# [#](https://programmercarl.com/0496.%E4%B8%8B%E4%B8%80%E4%B8%AA%E6%9B%B4%E5%A4%A7%E5%85%83%E7%B4%A0I.html#_496-%E4%B8%8B%E4%B8%80%E4%B8%AA%E6%9B%B4%E5%A4%A7%E5%85%83%E7%B4%A0-i)496.下一个更大元素 I

[力扣题目链接(opens new window)](https://leetcode.cn/problems/next-greater-element-i/)

给你两个 没有重复元素 的数组 nums1 和 nums2 ，其中nums1 是 nums2 的子集。

请你找出 nums1 中每个元素在 nums2 中的下一个比其大的值。

nums1 中数字 x 的下一个更大元素是指 x 在 nums2 中对应位置的右边的第一个比 x 大的元素。如果不存在，对应位置输出 -1 。

示例 1:

输入: nums1 = [4,1,2], nums2 = [1,3,4,2].  
输出: [-1,3,-1]  
解释:  
对于 num1 中的数字 4 ，你无法在第二个数组中找到下一个更大的数字，因此输出 -1 。  
对于 num1 中的数字 1 ，第二个数组中数字1右边的下一个较大数字是 3 。  
对于 num1 中的数字 2 ，第二个数组中没有下一个更大的数字，因此输出 -1 。

示例 2:  
输入: nums1 = [2,4], nums2 = [1,2,3,4].  
输出: [3,-1]  
解释:  
对于 num1 中的数字 2 ，第二个数组中的下一个较大数字是 3 。  
对于 num1 中的数字 4 ，第二个数组中没有下一个更大的数字，因此输出-1 。

提示：

- 1 <= nums1.length <= nums2.length <= 1000
- 0 <= nums1[i], nums2[i] <= 10^4
- nums1和nums2中所有整数 互不相同
- nums1 中的所有整数同样出现在 nums2 中

## 题解
仍然是单调栈的应用
注意

```
 index = nums1.index(nums2[stack[-1]])

 ans[index] = nums2[i]

```
这里算是一个细节

```python
 def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:

        stack = []

        ans = [-1]*len(nums1)

  

        for i in range(len(nums2)):

            while stack and nums2[i] > nums2[stack[-1]]:

                if nums2[stack[-1]] in nums1:

                    index = nums1.index(nums2[stack[-1]])

                    ans[index] = nums2[i]

                stack.pop()

            stack.append(i)

  

        return ans

```
# 503.下一个更大元素II

[力扣题目链接(opens new window)](https://leetcode.cn/problems/next-greater-element-ii/)

给定一个循环数组（最后一个元素的下一个元素是数组的第一个元素），输出每个元素的下一个更大元素。数字 x 的下一个更大的元素是按数组遍历顺序，这个数字之后的第一个比它更大的数，这意味着你应该循环地搜索它的下一个更大的数。如果不存在，则输出 -1。

示例 1:

- 输入: [1,2,1]
- 输出: [2,-1,2]
- 解释: 第一个 1 的下一个更大的数是 2；数字 2 找不到下一个更大的数；第二个 1 的下一个最大的数需要循环搜索，结果也是 2。

提示:

- 1 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9


## 题解
你可以把数组拼接一下，也可以遍历两次数组

下面展示遍历两次数组
```python
 def nextGreaterElements(self, nums: List[int]) -> List[int]:

        res = [-1]*len(nums)

        stack= []

  

        for i,num in enumerate(nums):

            while stack and num >nums[stack[-1]]:

                res[stack[-1]] = num

                stack.pop()

            stack.append(i)

  

        for num in nums:      

            if not stack:  

                return res

            while stack and num > nums[stack[-1]]:

                res[stack[-1]] = num

                stack.pop()

  

        return res
```
