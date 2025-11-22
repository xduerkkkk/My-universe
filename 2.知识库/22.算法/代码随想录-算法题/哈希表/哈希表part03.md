# [49. 字母异位词分组](https://leetcode.cn/problems/group-anagrams/)

中等

相关标签

![premium lock icon](https://static.leetcode.cn/cn-frontendx-assets/production/_next/static/images/lock-a6627e2c7fa0ce8bc117c109fb4e567d.svg)相关企业

给你一个字符串数组，请你将 字母异位词 组合在一起。可以按任意顺序返回结果列表。

**示例 1:**

**输入:** strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

**输出:** [["bat"],["nat","tan"],["ate","eat","tea"]]

**解释：**

- 在 strs 中没有字符串可以通过重新排列来形成 `"bat"`。
- 字符串 `"nat"` 和 `"tan"` 是字母异位词，因为它们可以重新排列以形成彼此。
- 字符串 `"ate"` ，`"eat"` 和 `"tea"` 是字母异位词，因为它们可以重新排列以形成彼此
## 思路
最笨的方法，一定是两个for循环， 比如第一个词eat，假如装入一个字典，
然后遍历第二个词一个一个减去，看如果减为0了说明第二个词是第一个词的异位词
能不能一个for循环？如何用到哈希表？


#   [451. 根据字符出现频率排序](https://leetcode.cn/problems/sort-characters-by-frequency/)


给定一个字符串 `s` ，根据字符出现的 **频率** 对其进行 **降序排序** 。一个字符出现的 **频率** 是它出现在字符串中的次数。

返回 _已排序的字符串_ 。如果有多个答案，返回其中任何一个。

**示例 1:**

**输入:** s = "tree"
**输出:** "eert"
**解释:** 'e'出现两次，'r'和't'都只出现一次。
因此'e'必须出现在'r'和't'之前。此外，"eetr"也是一个有效的答案

```python
class Solution:

    def frequencySort(self, s: str) -> str:

        counts = Counter(s)

  

        sorted_s = sorted(counts.items(), key = lambda item:item[1], reverse = True)

        res = []

        for char, freq in sorted_s:

            res.append(char * freq)

        return ''.join(res)

```
桶排序

```python
class Solution:
	 def frequencySort(self, s: str) -> str: 
		 counts = collections.Counter(s) 
		 max_freq = max(counts.values(), default=0) 
		 # 创建桶 
		 buckets = [[] for _ in range(max_freq + 1)] 
		 # 装桶 
		 for char, freq in counts.items(): 
			 buckets[freq].append(char) 
		# 倒出结果 
		 res = [] for i in range(max_freq, 0, -1):
		  # 从最大频率开始 
			  for char in buckets[i]: 
				  res.append(char * i) 
		return "".join(res)
```


# [347. 前 K 个高频元素](https://leetcode.cn/problems/top-k-frequent-elements/)


给你一个整数数组 `nums` 和一个整数 `k` ，请你返回其中出现频率前 `k` 高的元素。你可以按 **任意顺序** 返回答案。

## 频率排序

## 桶排序
