# 491 递增子序列
给你一个整数数组 `nums` ，找出并返回所有该数组中不同的递增子序列，递增子序列中 **至少有两个元素** 。你可以按 **任意顺序** 返回答案。

数组中可能含有重复元素，如出现两个整数相等，也可以视作递增序列的一种特殊情况。
## 题解
注意，当列表为空时，**布尔值为 `False`**
本题仍然是去重
需要注意的逻辑就是这一行

```
if (path and nums[i] < path[-1] ) or (nums[i] in used):
```


```python
def findSubsequences(self, nums: List[int]) -> List[List[int]]:

        ans = []

        path= []

        def backtrace(nums,start_index,path,ans):

            if len(path)>=2:

                ans.append(path[:])

            used = set()

            for i in range(start_index,len(nums)):

                if (path and nums[i] < path[-1] ) or (nums[i] in used):

                    continue

                used.add(nums[i])

                path.append(nums[i])

                backtrace(nums,i+1,path,ans)

                path.pop()

        backtrace(nums,0,path,ans)

        return ans

```
# 46 全排列
给定一个 没有重复 数字的序列，返回其所有可能的全排列。

示例:

- 输入: [1,2,3]
- 输出: [ [1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1] ]

## 题解

![[回溯part04-1749287961393.jpeg]]显然，我们这是纵向遍历，记录使用过的数字
那么我们还是像上一题，再每层递归的for循环之前定义used数组吗？
不对，上一题是横向遍历去重
那本题每次递归的时候，都要去检测used，是深度遍历的性质
可以定义used为全局变量。
pop和删除used标记是同步的，所以上图每一个节点下的used标记都是不变的。

```python
 def permute(self, nums: List[int]) -> List[List[int]]:

        path, ans = [], []

        used = set()

        def backtrace(nums,path,ans):

            if len(path) == len(nums):

                ans.append(path[:])

                return

            for i in range(len(nums)):

                if nums[i] in used:

                    continue

                used.add(nums[i])

                path.append(nums[i])

                backtrace(nums,path,ans)

                used.discard(nums[i])

                path.pop()

        backtrace(nums,path,ans)

        return ans

```
# 47 全排列II
给定一个可包含重复数字的序列 `nums` ，_**按任意顺序**_ 返回所有不重复的全排列。

**示例 1：**

**输入：**nums = [1,1,2]
**输出：**
[[1,1,2],
 [1,2,1],
 [2,1,1]]

## 题解

这里显然又是去重，本题的关键逻辑在这里：

```python
 if (i>0 and nums[i] == nums[i-1] and used[i-1] == 0) or used[i] == 1 :
```
一样的结合图看一下
![[回溯part04-1749302459026.jpeg]]
or used[i] == 1 ，是和上一题全排列题一样，这个条件判断和全排列II去重无关
i>0 and nums[i] == nums[i-1] and used[i-1] == 0 这个条件是横向去重
```python
def permuteUnique(self, nums: List[int]) -> List[List[int]]:

        path, ans = [], []

        nums.sort()

        used = [0] * len(nums)

  
  

        def backtrace(nums,path,ans):

            if len(path) == len(nums):

                ans.append(path[:])

                return

            for i in range(len(nums)):

                if (i>0 and nums[i] == nums[i-1] and used[i-1] == 0) or used[i] == 1 :

                    continue

                path.append(nums[i])

                used[i] = 1

                backtrace(nums,path,ans)

                path.pop()

                used[i] = 0

        backtrace(nums,path,ans)

        return ans

```
