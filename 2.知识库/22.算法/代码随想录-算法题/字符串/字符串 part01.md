# 344 反转字符串
## 题目描述
编写一个函数，其作用是将输入的字符串反转过来。输入字符串以字符数组 `s` 的形式给出。

不要给另外的数组分配额外的空间，你必须[原地](https://baike.baidu.com/item/%E5%8E%9F%E5%9C%B0%E7%AE%97%E6%B3%95)修改输入数组**、使用 O(1) 的额外空间解决这一问题。
## 题解
双指针，比较简单
```python
class Solution:

    def reverseString(self, s: List[str]) -> None:

        l = 0
        r = len(s) - 1
        
        for _ in range(len(s) // 2):     
            s[l], s[r] = s[r], s[l]
            l += 1
            r -= 1

```
# 541 反转字符串II
**字符串不可变**：在 Python 中，字符串是不可变对象，无法直接修改。如果需要频繁修改字符串（如反转、插入、删除等），通常会先转换成列表操作，最后用 `join()` 合并回字符串
如
```python
s = list("abcde") # 转为列表 
s[1:3] = ['X', 'Y'] # 修改部分字符 
result = ''.join(s) # 输出: "aXYde"

```

python的特性完美得避免一些边界判断

```python
    def reverseStr(self, s: str, k: int) -> str:

        s = list(s)

        for i in range(0,len(s),2*k):

            s[i:i+k] = s[i:i+k][::-1]

        return ''.join(s)

```
# 替换数字
## 题目描述
给定一个字符串 `s`，包含小写字母和数字字符，要求将字符串中的每个数字字符替换为 `"number"`，而字母字符保持不变。

**示例：**

- 输入：`"a1b2c3"` 输出：`"anumberbnumbercnumber"`
- 输入：`"a5b"` 输出：`"anumberb"`
## 题解

```python
def replace_digits_with_number(s):

result = [] 

for char in s: 
	if char.isdigit():
		 result.append("number") 
	else: 
	result.append(char) 
	
	return ''.join(result)

```
