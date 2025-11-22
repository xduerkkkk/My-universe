# 前置知识

| 类型                |                                |
| ----------------- | ------------------------------ |
| `dict`字典          | 存储键值对，快速查询，无法访问不存在的值           |
| `defaultdict`默认字典 | 存储键值对，快速查询，默认初始值0，访问不存在的值就原地创造 |
| `set`集合           | 如果和前两个对比，可以当作只存储键不存储值          |
# 242 有效的字母异位词


## 题目描述
给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的字母异位词。

示例 1: 输入: s = "anagram", t = "nagaram" 输出: true

示例 2: 输入: s = "rat", t = "car" 输出: false

**说明:** 你可以假设字符串只包含小写字母

## 题解

本题不能用集合哈，因为题目要求每个字母用的次数和原先的一样，所以我们要统计次数

```python
def isAnagram(self, s: str, t: str) -> bool:

        dic = defaultdict(int)


        for c in s:
            dic[c] += 1

        for c in t:
            dic[c] -= 1

  
        for i in dic.values():
            if i != 0:
                return False

        return True

```
# 346 两个数组的交集

题意：给定两个数组，编写一个函数来计算它们的交集。

set可以直接将列表解析
![[哈希表part01-1747652590734.jpeg]]
一步到位法：
```python
 def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:

        return list(set(nums1) & set(nums2))

```
集合法：
```python

		set_1 = set(nums1)
        set_2 = set()

        for num_2 in nums2:

            if num_2 in set_1 :

                set_2.add(num_2)

  

        ans = list(set_2) #将集合转化为列表

        return ans

```
# 202快乐数
## 题目描述
编写一个算法来判断一个数 n 是不是快乐数。

「快乐数」定义为：对于一个正整数，每一次将该数替换为它每个位置上的数字的平方和，然后重复这个过程直到这个数变为 1，也可能是 无限循环 但始终变不到 1。如果 可以变为  1，那么这个数就是快乐数。

如果 n 是快乐数就返回 True ；不是，则返回 False
## 题解
主要是，“无限循环”，要理解好。不要理解成“无限不循环”了，回忆一下小学学的无限（不）循环小数。
也就是说，若不是快乐数，计算的数会重复出现

优化前： get_sum命名不合适  计算方法不高级（emm 不正规吧）
```python
def get_sum(num) -> int:

            sum = 0

            for digital in str(num):

                sum += int(digital) * int( digital)

            return sum

  

        record = set()

        while n not in record:

            if n == 1:

                return True

            record.add(n)

            n = get_sum(n)

  

        return False

```
优化后

```python
	def get_next(n: int) -> int:
	        total = 0
	        while n > 0:
	            n, digit = divmod(n, 10)
	            total += digit ** 2
	        return total
	
	    seen = set()
	    
	    while n not in seen:
	        if n == 1:
	            return True
	        seen.add(n)
	        n = get_next(n)
	    
	    return False


```
**判断是否已见、是否为 1、添加新值这三步顺序必须严谨**
不然像下面这样，刚加入seen集合，下一步就跳出循环了
```python
		while n not in seen:
			n = get_next(n)
			if n == 1:
	            return True
	        seen.add(n)
	

```
快慢指针法
昨天讲的，若有环，快慢指针则可以判断，这里也可以用。
```python
slow_runner = n
    fast_runner = get_next(n)
    while fast_runner != 1 and slow_runner != fast_runner:
        slow_runner = get_next(slow_runner)
        fast_runner = get_next(get_next(fast_runner))
    return fast_runner == 1

```
# 1 两数之和
## 题目描述
给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。

你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。

**示例:**

给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9

所以返回 [0, 1]
## 题解
本来在想滑动窗口，然后发现这个不能排序（而滑动窗口的前提是有序），因为要返回下标
然后就偷懒看题解了，看了眼思路自己敲一遍
思路是创建字典！ 字典记录键值对是 数：下标
循环nums列表（时间复杂度n）时，直接靠搜索键值看有没有匹配的数（时间复杂度1，正是这里比起两个for循环的O（$n^2$）更好）


注意，enumerate（列表/字典），先返回的是index，在返回的value


```python
 def twoSum(self, nums: List[int], target: int) -> List[int]:

        seen = dict()

  

        for index, value in enumerate(nums):

            if target - value in seen:

                return [index , seen[target - value] ]

            else:

                seen[value] = index

  

        return []

```

