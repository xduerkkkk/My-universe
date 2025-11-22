# 前置小知识
### Counter
输入可以是列表，也可以是字符串。最终把他们转化成字典，值为出现次数。
访问不存在的，会创建并给出‘0’的值
这一点像昨天介绍的defualtdict的字典版本

```python
from collections import Counter

fruits = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
counter = Counter(fruits)

print(counter)
# 输出: Counter({'apple': 3, 'banana': 2, 'orange': 1})

```

### dict.get()

| `dict[key]`               | 返回值 | 抛出`KeyError` | ❌   |
| ------------------------- | --- | ------------ | --- |
| `dict.get(key)`           | 返回值 | 返回`None`     | ✅   |
| `dict.get(key, 自定义返回的东西)` | 返回值 | 返回"自定义返回的东西" | ✅   |
注意，defualtdict也可以用get方法，用法与dict一模一样！
# 454 四数相加II
## 题目描述
给你四个整数数组 `nums1`、`nums2`、`nums3` 和 `nums4` ，数组长度都是 `n` ，请你计算有多少个元组 `(i, j, k, l)` 能满足：

- `0 <= i, j, k, l < n`
- `nums1[i] + nums2[j] + nums3[k] + nums4[l] == 0`

**示例 1：**

**输入：nums1 = [1,2], nums2 = [-2,-1], nums3 = [-1,2], nums4 = [0,2]**
输出：**2
解释：
两个元组如下：
1. (0, 0, 0, 1) -> nums1[0] + nums2[0] + nums3[0] + nums4[1] = 1 + (-2) + (-1) + 2 = 0
2. (1, 1, 0, 0) -> nums1[1] + nums2[1] + nums3[0] + nums4[0] = 2 + (-1) + (-1) + 0 = 0
## 题解
暴力解法显然需要O（n的四次方）
我们可以简化一下，将4个数组变成两个数组，前两个

先来个自己写的错误版本

```python
hash = defaultdict(int)

        for x in nums1:

            for y in nums2:

                hash[x+y] = 1

        count = 0

        for x in nums3:

            for y in nums4:

                if -(x+y) in hash:

                    count += 1

  

        return count

```
#### 两个问题
- hash[x+y] = 1是问题所在，没有更新次数。
- count += 1也是问题所在。 
- 写出这种错误代码是没搞清抵消逻辑。比如nums1和nums2的搭配中，有三次搭配出”2“，记hash[2]的值为3.那么在后面的num3num4循环录，只要一次循环中，nums3和nums4中搭配出一个2，这个2就立刻能与之前的三次"2"相加为0，Counter立刻加3。
```python
if -(x+y) in hash:
				count += hash[-(x+y)]
```
#### 优化
hash优化
```python
hash = Counter(x + y for x in nums1 for y in nums2)

```
后半段返回count优化：

```python
return sum(hash[-x-y] for x in nums3 for y in nums4)
```
最后可以优化成两行代码
```python
 def fourSumCount(self, nums1: List[int], nums2: List[int], nums3: List[int], nums4: List[int]) -> int:

        hash = Counter(x + y for x in nums1 for y in nums2)

        return sum(hash[-x-y] for x in nums3 for y in nums4)

```

# 383 赎金信
## 题目描述
给你两个字符串：`ransomNote` 和 `magazine` ，判断 `ransomNote` 能不能由 `magazine` 里面的字符构成。

如果可以，返回 `true` ；否则返回 `false` 。

`magazine` 中的每个字符只能在 `ransomNote` 中使用一次。
## 题解
```python
def canConstruct(self, ransomNote: str, magazine: str) -> bool:

        seen = defaultdict(int)

        for s in magazine:

            seen[s] += 1

        for s in ransomNote:

            seen[s] -= 1

            if seen[s] < 0:

                return False

  

        return True

```
### 优化：
seen = Counter（ransomNote）可替代

```python
  seen = defaultdict(int)

        for s in magazine:

            seen[s] += 1

```
嗯，如果用上counter，也可以一行解决
只不过性能不够，但一行代码很酷就是了
```python
 def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        return Counter(ransomNote) <= Counter(magazine)

作者：灵茶山艾府
链接：https://leetcode.cn/problems/ransom-note/solutions/3643383/jian-dan-ti-jian-dan-zuo-pythonjavaccgoj-nh3q/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```
PS： 很多简洁版本都是来自 灵茶山艾府


# 15 三数之和
## 题目描述
给你一个整数数组 `nums` ，判断是否存在三元组 `[nums[i], nums[j], nums[k]]` 满足 `i != j`、`i != k` 且 `j != k` ，同时还满足 `nums[i] + nums[j] + nums[k] == 0` 。请你返回所有和为 `0` 且不重复的三元组。

**注意：**答案中不可以包含重复的三元组。
## 题解
重要思想：排序、双指针

```python
 def threeSum(self, nums: List[int]) -> List[List[int]]:

        nums.sort()

        ans = []

        for i in range(len(nums)):

            if nums[i] > 0:

                return ans


            if i > 0 and nums[i] == nums[i - 1]:

                continue  

            left = i+1

            right = len(nums) - 1

  
            while left < right:

                sum_ = nums[i] + nums[left] + nums[right]



                if sum_ > 0:

                    right -= 1

                elif sum_ <0:

                    left += 1

                else:

                    ans.append([nums[i] , nums[left] , nums[right]])

                    while left < right and nums[left] == nums[left + 1]:

                            left += 1

                    while left < right and nums[right] == nums[right - 1]:

                            right -= 1

  
                    right -= 1

                    left += 1

        return ans

```


# 18 四数之和
比起三数之和多一层循环

```python

class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        result = []
        for i in range(n):
            if nums[i] > target and nums[i] > 0 and target > 0:# 剪枝（可省）
                break
            if i > 0 and nums[i] == nums[i-1]:# 去重
                continue
            for j in range(i+1, n):
                if nums[i] + nums[j] > target and target > 0: #剪枝（可省）
                    break
                if j > i+1 and nums[j] == nums[j-1]: # 去重
                    continue
                left, right = j+1, n-1
                while left < right:
                    s = nums[i] + nums[j] + nums[left] + nums[right]
                    if s == target:
                        result.append([nums[i], nums[j], nums[left], nums[right]])
                        while left < right and nums[left] == nums[left+1]:
                            left += 1
                        while left < right and nums[right] == nums[right-1]:
                            right -= 1
                        left += 1
                        right -= 1
                    elif s < target:
                        left += 1
                    else:
                        right -= 1
        return result


```

后两道题提醒我，剪枝去重也很重要！