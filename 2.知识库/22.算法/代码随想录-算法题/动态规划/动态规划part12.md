# 115.不同的子序列

[力扣题目链接(opens new window)](https://leetcode.cn/problems/distinct-subsequences/)

给定一个字符串 s 和一个字符串 t ，计算在 s 的子序列中 t 出现的个数。

字符串的一个 子序列 是指，通过删除一些（也可以不删除）字符且不干扰剩余字符相对位置所组成的新字符串。（例如，"ACE" 是 "ABCDE" 的一个子序列，而 "AEC" 不是）

题目数据保证答案符合 32 位带符号整数范围。
## 题解
 确定dp数组（dp table）以及下标的含义
`dp[i][j]`：以i-1为结尾的s子序列中出现以j-1为结尾的t的个数为`dp[i][j]`
![[动态规划part12-1751082913432.jpeg]]

### 决策的本质：你有两种选择权

当 `s` 和 `t` 的末尾字符相等时（如 `s[i-1] = 'g'`, `t[j-1] = 'g'`），
这么想，我们要在s里面找t对不对？
ba先不管，看看g，s里面有两个g诶，那是不是有可能最终s选的bag的g，是最后一个g，即末尾项相同的这个g，也有可能是前面的g，在这个例子中就是babg的g，`s[3]` 

所以，当末尾字符串相等时，我们面临两种互不冲突的决策：

1. ​**选择①：用这个 `g` 匹配掉 `t` 的 `g`**​  
    → 问题转化为：​**剩下的 `s[0:i-2]` 需匹配剩下的 `t[0:j-2]`**​  
    → 对应 `dp[i-1][j-1]`  
    ​**物理意义**​：`s` 的前 `i-1` 个字符（`babgba`）需匹配 `t` 的前 `j-1` 个字符（`ba`）。
    
2. ​**选择②：不用这个 `g` 匹配 `t` 的 `g`**​  
    → 问题转化为：​**剩下的 `s[0:i-2]` 需匹配完整的 `t[0:j-1]`**​  
    → 对应 `dp[i-1][j]`  
    ​**物理意义**​：`s` 的前 `i-1` 个字符（`babgba`）需匹配 `t` 的全部 `j` 个字符（`bag`）。
    

> ✅ ​**关键**​：这两种选择是**完全独立且互斥的**，因此总方案数是它们的和。

代码核心为状态方程：

```python

                if s[i-1] == t[j-1]:

                    dp[i][j] = dp[i-1][j-1] + dp[i-1][j]

                else:

                    dp[i][j] = dp[i-1][j]
```
![[动态规划part12-1751084316392.jpeg]]


完整代码：
```python
def numDistinct(self, s: str, t: str) -> int:

        n_s = len(s)

        n_t = len(t)

        dp = [[0]*(n_t+1) for _ in range(n_s+1)]

  

        for i in range(n_s+1):

            dp[i][0] = 1

        for i in range(1,n_t+1):

            dp[0][i] = 0

  

        for i in range(1,n_s+1):

            for j in range(1,n_t+1):

                if s[i-1] == t[j-1]:

                    dp[i][j] = dp[i-1][j-1] + dp[i-1][j]

                else:

                    dp[i][j] = dp[i-1][j]

  

        return dp[-1][-1]
```
# 583. 两个字符串的删除操作

[力扣题目链接(opens new window)](https://leetcode.cn/problems/delete-operation-for-two-strings/)

给定两个单词 word1 和 word2，找到使得 word1 和 word2 相同所需的最小步数，每步可以删除任意一个字符串中的一个字符。

示例：

- 输入: "sea", "eat"
- 输出: 2
- 解释: 第一步将"sea"变为"ea"，第二步将"eat"变为"ea"
## 题解
确定dp数组（dp table）以及下标的含义
`dp[i][j]：以i-1为结尾的字符串word1，和以j-1位结尾的字符串word2，想要达到相等，所需要删除元素的最少次数。`
**`当word1[i - 1] 与 word2[j - 1]相同的时候，dp[i][j] = dp[i - 1][j - 1];`**
因为多出的那一个相同的字符，要删就一起删了
举两个例子
`dpa p    和    dpab  pb         dpa p  和 dpap   pp`
是不是无论如何都是删除`da`呢？？上面几种情况都是两次删除

`当word1[i - 1] 与 word2[j - 1]相同的时候，dp[i][j] = dp[i - 1][j - 1];
`
`当word1[i - 1] 与 word2[j - 1]不相同的时候，我们要进行删除操作：`
在讲情况前，说一下为啥要删除。回顾题目，要求进行一定删除操作后留下公共序列对吧？那只要不同了，怎么可能保留他们呢？不同的字符，怎么会保留？ 所以一定要删除，至于怎么删，有三种情况，这三种情况不是我们“逻辑思考”的得出的，而是现实中的“删除”操作就这两种。就好比我问你明天天气有哪些情况，你可以毫不犹豫说能看见太阳的和看不见太阳的，这其中没有任何逻辑推演！ 这就是动态规划的妙处之一。 
三种情况：
`情况一：删word1[i - 1]，最少操作次数为dp[i - 1][j] + 1

`情况二：删word2[j - 1]，最少操作次数为dp[i][j - 1] + 1

`情况三：同时删word1[i - 1]和word2[j - 1]，操作的最少次数为dp[i - 1][j - 1] + 2`


核心代码
```python
 for i in range(1,n1+1):

            for j in range(1, n2+1):

                if word1[i-1] == word2[j-1]:

                    dp[i][j] = dp[i-1][j-1]

                else:

                    dp[i][j] = min(dp[i-1][j-1]+2, dp[i-1][j]+1, dp[i][j-1]+1)
```
再就是注意初始化。
完整代码：

```python
def minDistance(self, word1: str, word2: str) -> int:

        n1 = len(word1)

        n2 = len(word2)

  

        dp = [[0]*(n2+1) for _ in range(n1+1)]

        for i in range(n1+1):

            dp[i][0] = i

        for j in range(1,n2+1):

            dp[0][j] = j

  

        for i in range(1,n1+1):

            for j in range(1, n2+1):

                if word1[i-1] == word2[j-1]:

                    dp[i][j] = dp[i-1][j-1]

                else:

                    dp[i][j] = min(dp[i-1][j-1]+2, dp[i-1][j]+1, dp[i][j-1]+1)

        return dp[-1][-1]

```

# 72. 编辑距离

[力扣题目链接(opens new window)](https://leetcode.cn/problems/edit-distance/)

给你两个单词 word1 和 word2，请你计算出将 word1 转换成 word2 所使用的最少操作数 。

你可以对一个单词进行如下三种操作：

- 插入一个字符
    
- 删除一个字符
    
- 替换一个字符
    
- 示例 1：
    
- 输入：word1 = "horse", word2 = "ros"
    
- 输出：3
    
- 解释： horse -> rorse (将 'h' 替换为 'r') rorse -> rose (删除 'r') rose -> ros (删除 'e')
    
- 示例 2：
    
- 输入：word1 = "intention", word2 = "execution"
    
- 输出：5
    
- 解释： intention -> inention (删除 't') inention -> enention (将 'i' 替换为 'e') enention -> exention (将 'n' 替换为 'x') exention -> exection (将 'n' 替换为 'c') exection -> execution (插入 'u')
    

提示：

- 0 <= word1.length, word2.length <= 500
- word1 和 word2 由小写英文字母组成
## 题解
```
if (word1[i - 1] == word2[j - 1])
    不操作
if (word1[i - 1] != word2[j - 1])
    增
    删
    换
```
`word1[i - 1] == word2[j - 1]` 就不用操作了，这个好理解
主要看看`word1[i - 1] != word2[j - 1]` 

- 操作一：word1删除一个元素，那么就是以下标i - 2为结尾的word1 与 j-1为结尾的word2的最近编辑距离 再加上一个操作。

即 `dp[i][j] = dp[i - 1][j] + 1;`

- 操作二：word2删除一个元素，那么就是以下标i - 1为结尾的word1 与 j-2为结尾的word2的最近编辑距离 再加上一个操作。

即 `dp[i][j] = dp[i][j - 1] + 1;`

- 操作三：添加元素：**word2添加一个元素，相当于word1删除一个元素**，例如 `word1 = "ad" ，word2 = "a"`，`word1`删除元素`'d'` 和 `word2`添加一个元素`'d'`，变成`word1="a", word2="ad"`， 最终的操作数是一样！
- 操作四:替换元素，
即`dp[i][j] = dp[i - 1][j - 1] + 1;`

对于dp的初始化，和“两个字符串的删除操作初始化一样一样的。
核心代码，状态转移方程：

```python
  for i in range(1, len(word1)+1):
            for j in range(1, len(word2)+1):
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1]) + 1
```

最终代码
```python
def minDistance(self, word1: str, word2: str) -> int:
        dp = [[0] * (len(word2)+1) for _ in range(len(word1)+1)]
        for i in range(len(word1)+1):
            dp[i][0] = i
        for j in range(len(word2)+1):
            dp[0][j] = j
        for i in range(1, len(word1)+1):
            for j in range(1, len(word2)+1):
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1]) + 1
        return dp[-1][-1]
```
