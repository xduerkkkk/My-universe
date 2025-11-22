# 150 逆波兰表达式求值
## 题目描述
给你一个字符串数组 `tokens` ，表示一个根据 [逆波兰表示法](https://baike.baidu.com/item/%E9%80%86%E6%B3%A2%E5%85%B0%E5%BC%8F/128437) 表示的算术表达式。

请你计算该表达式。返回一个表示表达式值的整数。
## 题解


```python
def evalRPN(self, tokens: List[str]) -> int:

        stack = []

        op_map = {

        '+': lambda x, y: x + y,

        '-': lambda x, y: x - y,

        '*': lambda x, y: x * y,

        '/': lambda x, y: int(x / y)

        }

        for token in tokens:

            if token in op_map:

                op1 = stack.pop()

                op2 = stack.pop()

                result = op_map[token](op2, op1)

                stack.append(result)

            else:

                stack.append(int(token))

        return stack.pop()

```
# 239 滑动窗口最大值
## 题目描述
给你一个整数数组 `nums`，有一个大小为 `k` 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 `k` 个数字。滑动窗口每次只向右移动一位。

返回 _滑动窗口中的最大值_ 。
## 题解
最简单能想到的是暴力解法
```python
 def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:

        left = 0

        right = k - 1

        ans = []

        while (right < len(nums)):

            ans.append(max(nums[left:right+1]))

            left += 1

            right += 1

  

        return ans

```
时间复杂度巨巨高，是nk！
python对列表的切片还会产生新的空间，
所以空间复杂度也巨巨高
且这个方法没什么思想的含金量
如何优化呢？

首先整体思路是，大的进来，大数前面的小数都可以走开了，你们对接下来的“判断最大值”没用了。
接着做好边界处理，保证窗口外的数也走开

```python
	if nums[i - k] == deque[0]:
               deque.popleft()

```
   
还要注意，窗口形成时（最开始那三个）和形成后，逻辑稍微不同

```python
def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:

        deque = collections.deque()

        ans = []

  

        for i in range(k):

            while deque and nums[i] > deque[-1]:

                deque.pop()

	            deque.append(nums[i])

        ans.append(deque[0])

  

        for i in range(k,len(nums)):

            if nums[i - k] == deque[0]:

                deque.popleft()

            while deque and nums[i] > deque[-1]:

                deque.pop()

            deque.append(nums[i])

            ans.append(deque[0])

  

        return ans

```
不同在哪呢，放大看看哈
形成窗口时
```python
		while deque and nums[i] > deque[-1]:

                deque.pop()

	            deque.append(nums[i])

        ans.append(deque[0])


```
形成窗口后

```python
		while deque and nums[i] > deque[-1]:

                deque.pop()

	    deque.append(nums[i])

        ans.append(deque[0])


```


# 347 前k个高频元素
## 题目描述
给你一个整数数组 `nums` 和一个整数 `k` ，请你返回其中出现频率前 `k` 高的元素。你可以按 **任意顺序** 返回答案。
## 题解
自己歪打正着的

```python
		dict1 = defaultdict(int)

        for item in nums:

            dict1[item]+= 1

        times = list(dict1.values())

        times.sort(reverse=True)

  

        values = times[:k]

        ans = []

        for key in dict1:

            if dict1[key] in values:

                ans.append(key)

        return ans[:k]

```
这个方法导致输出**顺序依赖字典遍历顺序**，无法保证唯一性，不稳定。
同时排序以及nlogn了，再次遍历字典又有O（n* k ）的时间复杂度，整体解决n方。
而且代码而繁琐 不如三行代码：

```python
		freq = Counter(nums)

        # 按频率从高到低排序
        sorted_freq = sorted(freq.items(), key=lambda x: -x[1])

        # 返回前 k 个元素的数字部分
        return [item for item, _ in sorted_freq[:k]]

```
时间复杂度还是nlogn


当然，借助本题我们要学习的是python中的
*heapq* 数据结构，**小顶堆**
headpop是将最小的元素pop掉


```python
		dict1 = defaultdict(int)

        for item in nums:

            dict1[item]+= 1


		heap = []

        for num, count in dict1.items():

            heappush(heap,(count,num))

            if len(heap) > k:

                heappop(heap)

        return [num for count, num in heap]

```
注意：
`for num, count in dict1:`是错误的

`dict1 = Counter(nums)`也是可以的


还有个桶排序、手动实现heapq可以学学，
二刷来