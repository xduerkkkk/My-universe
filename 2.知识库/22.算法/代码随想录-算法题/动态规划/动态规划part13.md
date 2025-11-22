# 647. 回文子串

[力扣题目链接(opens new window)](https://leetcode.cn/problems/palindromic-substrings/)

给定一个字符串，你的任务是计算这个字符串中有多少个回文子串。

具有不同开始位置或结束位置的子串，即使是由相同的字符组成，也会被视作不同的子串。

示例 1：

- 输入："abc"
- 输出：3
- 解释：三个回文子串: "a", "b", "c"

示例 2：

- 输入："aaa"
- 输出：6
- 解释：6个回文子串: "a", "a", "a", "aa", "aa", "aaa"

提示：输入的字符串长度不会超过 1000 。

## 题解
显然双指针还是最适合回文数之类的题
以中心为扩散，双指针配合检验是否为回文串
```python
 def countSubstrings(self, s: str) -> int:
        result = 0
        for i in range(len(s)):
            result += self.extend(s, i, i, len(s)) #以i为中心
            result += self.extend(s, i, i+1, len(s)) #以i和i+1为中心
        return result
    
    def extend(self, s, i, j, n):
        res = 0
        while i >= 0 and j < n and s[i] == s[j]:
            i -= 1
            j += 1
            res += 1
        return res
```
当然我们还得练习动规
本题不再考感觉了，我们得严格按照动态规划步骤
1. 动态数组的定义：将大问题拆解为一个个小问题，按之前的套路我们下意识地会设 ` dp[i] 为 下标i结尾的字符串有 dp[i]个回文串的话，我们会发现很难找到递归关系。dp[i] 和 dp[i-1] ，dp[i + 1] 看上去都没啥关系。判断字符串S是否是回文，那么如果我们知道 s[1]，s[2]，s[3] 这个子串是回文的，那么只需要比较 s[0]和s[4]这两个元素是否相同，如果相同的话，这个字符串s 就是回文串。`于是我们`设dp[i][j] 为s[i] 到 s[j] 是否为回文字符串返回True或False ，符合回文串定义
2. 递推公式：大范围只有两种情况：
    -  `s[i]与s[j]` 相等:注意，i与j之间有可能有字符串，有可能都没有字符串。给出三种情况，前两种为中间没有字符串，最后一种是有字符串1.若i与j相等，则为回文字符串 2.若j比i大1，是回文字符串 3. j比i大2及以上，若包含的这个字符串即`dp[i + 1][j - 1]` 为True(是回文字符串)，则整体为回文字符串
    - `s[i]与s[j]` 不相等： 不是回文字符串
3. 初始化：根据递推公式确定遍历顺序，一个状态要用到左下角的状态，那一定要从左忘右，从下到上![[动态规划part13-1751165065034.jpeg]]
代码：
```python
  def countSubstrings(self, s: str) -> int:
        dp = [[False] * len(s) for _ in range(len(s))]
        result = 0
        for i in range(len(s)-1, -1, -1): #注意遍历顺序
            for j in range(i, len(s)):
                if s[i] == s[j]:
                    if j - i <= 1: #情况一 和 情况二
                        result += 1
                        dp[i][j] = True
                    elif dp[i+1][j-1]: #情况三
                        result += 1
                        dp[i][j] = True
        return result
```

# 516.最长回文子序列

[力扣题目链接(opens new window)](https://leetcode.cn/problems/longest-palindromic-subsequence/)

给定一个字符串 s ，找到其中最长的回文子序列，并返回该序列的长度。可以假设 s 的最大长度为 1000 。

示例 1: 输入: "bbbab" 输出: 4 一个可能的最长回文子序列为 "bbbb"。

示例 2: 输入:"cbbd" 输出: 2 一个可能的最长回文子序列为 "bb"。

提示：

- 1 <= s.length <= 1000
- s 只包含小写英文字母
## 题解
```python
   def longestPalindromeSubseq(self, s: str) -> int:
        dp = [[0] * len(s) for _ in range(len(s))]
        for i in range(len(s)):
            dp[i][i] = 1
        for i in range(len(s)-1, -1, -1):
            for j in range(i+1, len(s)):
                if s[i] == s[j]:
                    dp[i][j] = dp[i+1][j-1] + 2
                else:
                    dp[i][j] = max(dp[i+1][j], dp[i][j-1])
        return dp[0][-1]
```