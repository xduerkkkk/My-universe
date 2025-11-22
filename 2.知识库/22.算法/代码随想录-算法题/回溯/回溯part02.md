# 39.组合总和
给你一个 **无重复元素** 的整数数组 `candidates` 和一个目标整数 `target` ，找出 `candidates` 中可以使数字和为目标数 `target` 的 所有 **不同组合** ，并以列表形式返回。你可以按 **任意顺序** 返回这些组合。

`candidates` 中的 **同一个** 数字可以 **无限制重复被选取** 。如果至少一个数字的被选数量不同，则两种组合是不同的。 

对于给定的输入，保证和为 `target` 的不同组合数少于 `150` 个。

**示例 1：**

**输入：candidates = `[2,3,6,7]`, target = `7`
输出：[[2,2,3],[7]]
解释：
2 和 3 可以形成一组候选，2 + 2 + 3 = 7 。注意 2 可以使用多次。
7 也是一个候选， 7 = 7 。
仅有这两种组合。

## 题解

```python
class Solution:

    def backtrace(self,candidates, target, current_sum, startindex, path, result):

        if current_sum > target:

            return

        if current_sum == target:

            result.append(path[:])

            return

        for i in range(startindex, len(candidates)):

            current_sum += candidates[i]

            path.append(candidates[i])

            self.backtrace(candidates,target,current_sum,i,path,result)

            current_sum -= candidates[i]

            path.pop()

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:

        result, path = [], []

        self.backtrace(candidates, target, 0, 0, path, result)

        return result

```
与昨天的回溯有何不同？
我们现在是可以重复数字的，
所以递归中传入的是‘i’，而不是‘i+1'

```python
self.backtrace(candidates,target,current_sum,i,path,result)
```
## 小细节
如果我们排序
```
candidates.sort()
```
便可以在每次的for循环里加入
```
if current_sum + candidates[i] > target:
                break
```
避免不必要的遍历
# 40.组合总和 II
给定一个候选人编号的集合 `candidates` 和一个目标数 `target` ，找出 `candidates` 中所有可以使数字和为 `target` 的组合。

`candidates` 中的每个数字在每个组合中只能使用 **一次** 。

**注意：**解集不能包含重复的组合。 

**示例 1:**

**输入:** candidates = `[10,1,2,7,6,1,5]`, target = `8`,
**输出:**
[
[1,1,6],
[1,2,5],
[1,7],
[2,6]
]
## 题解

```python
class Solution:

    def backtrace(self,candidates, target, current_sum, start_index, path, result):

         if current_sum == target:

            result.append(path[:])

            return

         for i in range(start_index, len(candidates)):

            if i > start_index and candidates[i] == candidates[i-1]:

                continue

            if current_sum + candidates[i] > target:

                break

            current_sum += candidates[i]

            path.append(candidates[i])

            self.backtrace (candidates, target, current_sum, i+1, path, result)

            current_sum -= candidates[i]

            path.pop()

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:

        result, path = [], []

        candidates.sort()

        self.backtrace(candidates, target, 0, 0, path, result)

        return result

```

# 131 分割回文串
给你一个字符串 `s`，请你将 `s` 分割成一些 子串，使每个子串都是 **回文串** 。返回 `s` 所有可能的分割方案
## 题解
首先要实现的一个东西是判断回文
双指针
**空间效率高**：无需额外内存（空间复杂度 `O(1)`），适合大字符串或内存敏感场景
但代码稍微复杂，且小字符串速度不快
切片逆序拷贝
- **执行速度快**：切片操作在 Python 中由底层优化，对小字符串效率极高。
- 但 **空间开销**：切片会生成新字符串（空间复杂度 `O(n)`），超大字符串可能影响性能。

我们既然python了，就选切片吧

对于本题的回溯，继续强调一点
回溯是“深度优先遍历”，我们是一路到最左下角的a|a|b，接着再回溯到第一个红叉（ab不是回文这一步），再回溯到截取aa
![[回溯part02-1749181769819.jpeg]]
```python


    def partition(self, s: str) -> List[List[str]]:
        result = []
        self.backtracking(s, 0, [], result)
        return result

    def backtracking(self, s, start_index, path, result ):
        # Base Case
        if start_index == len(s):
            result.append(path[:])
            return
        
        # 单层递归逻辑
        for i in range(start_index, len(s)):
            # 若反序和正序相同，意味着这是回文串
            if s[start_index: i + 1] == s[start_index: i + 1][::-1]:
                path.append(s[start_index:i+1])
                self.backtracking(s, i+1, path, result)   # 递归纵向遍历：从下一处进行切割，判断其余是否仍为回文串
                path.pop()             # 回溯
```