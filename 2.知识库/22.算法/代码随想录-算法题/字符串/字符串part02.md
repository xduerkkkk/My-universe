# 151 反转字符串中的单词
## 题目描述
给你一个字符串 `s` ，请你反转字符串中 **单词** 的顺序。

**单词** 是由非空格字符组成的字符串。`s` 中使用至少一个空格将字符串中的 **单词** 分隔开。

返回 **单词** 顺序颠倒且 **单词** 之间用单个空格连接的结果字符串。

**注意：**输入字符串 `s`中可能会存在前导空格、尾随空格或者单词间的多个空格。返回的结果字符串中，单词间应当仅用单个空格分隔，且不包含任何额外的空格。
## 题解
正常思路的话考点有这么几个：
- 删除字符串前后空格
- 反转字符串（先整体反转，再分别反转）
但是python又不一样了
请看split函数

```python
text = "Hello World"
result = text.split()
print(result)  # 输出：['Hello', 'World']
```
字符串变列表除了是python标准做法了，可以回顾一下昨天的字符串part01
reverse函数也是针对列表的方法

```python
fruits = ["apple", "banana", "cherry"]
fruits.reverse()
print(fruits)  # 输出：['cherry', 'banana', 'apple']

```
我们不使用字符串的切片方法，它会所有的都反转过来。字符串的切片方法如下

```python
text = "hello world"
reversed_text = text[::-1]
print(reversed_text)  # 输出：'dlrow olleh'

```
但是列表使用切片符合题意
```python
text = "hello world"
# 使用 split() 分割句子为单词列表
words = text.split()
# 使用切片操作反转单词列表的顺序
words = words[::-1]
```
输出结果将是：
`['world', 'hello']`


所以是字符串转换成列表，
再使用列表的reverse方法
最后再通过join把列表变成字符串

```python
def reverseWords(self, s: str) -> str:

        s = s.strip() # 删除空格

        strs = s.split()  # 字符串转换成列表

        strs.reverse()  # 或strs=strs[::1]

        return ' '.join(strs)

```
# KMP算法
分为两步
算公共前后缀表、借助此表进行高效率地匹配
## next表
假设我们的needle是- `s = "abababc"`
我们手动算一下前缀表，应该是0 0 1 2 3 4 0
```python

next = [0] * len(needle)

def getNext(self, next, s):      
		j = 0
        next[0] = 0
        for i in range(1, len(s)):
            while j > 0 and s[i] != s[j]:
                j = next[j - 1]
            if s[i] == s[j]:
                j += 1
            next[i] = j
```
j指向前缀末尾位置，i指向后缀末尾位置
j指向前缀末尾位置，i指向后缀末尾位置
j指向前缀末尾位置，i指向后缀末尾位置！！！
abababc为例子，第一个for循环，分析的是ab，i与j不相同，ab没有公共前后缀，那j继续待着，i往后走开始分析aba。此时for循环让i走到了第三个a，呀！那和j所处位置相同，
好，那么aba这里，最长公共前后缀是1了， 接着i和j同时走，又相等了！abab这里，最长公共前后缀是2了...
一直到ababab对吧！ i与j始终共同前进一步----》 发现相等。可当i走到最后一个，也就是此时函数分析abababc 
`while j > 0 and s[i] != s[j]:`  j一路往左，变成0
看看，如果字符串是abababa呢？    
对于ababab 0 0 1 2 3 4
i此时是最后一个a，j此时是第二个b。不相等！`j = next[j - 1]`等价 j往左一步，呀，相等了。

```python
			if s[i] == s[j]:
                j += 1
            next[i] = j

```
next表的最后一格是3
abababa  0 0 1 2 3 4 3

## 借助前缀表进行KMP

```python

def strStr(self, haystack: str, needle: str) -> int:
        if len(needle) == 0:
            return 0
        next = [0] * len(needle)
        self.getNext(next, needle) #此处完成了next的更新
        j = 0
        for i in range(len(haystack)):
            while j > 0 and haystack[i] != needle[j]:
                j = next[j - 1]
            if haystack[i] == needle[j]:
                j += 1
            if j == len(needle):
                return i - len(needle) + 1
        return -1
```

