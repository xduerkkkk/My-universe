# 77组合
给定两个整数 `n` 和 `k`，返回范围 `[1, n]` 中所有可能的 `k` 个数的组合。

你可以按 **任何顺序** 返回答案。
## 题解


```python
def combine(self, n: int, k: int) -> List[List[int]]:

        result = []

        path = []

        self.backtrace(n, k, 1, path, result)

        return result

  

    def backtrace(self, n, k, start, path, result):

        if len(path) == k:

            result.append(path[:])

            return

        for i in range(start, n+1):

            path.append(i)

            self.backtrace( n, k, i+1, path, result)

            path.pop()

```
最关键的部分，是这四行，执行递归的逻辑
```python
		for i in range(start, n+1):
		
			path.append(i)

            self.backtrace( n, k, i+1, path, result)

            path.pop()
```
初始的path.append(i) 使得path：
[]   --->   [1]     
接着又进入函数，此时函数携带的初始信息是[1]
再次path.append(i) 
[1] ----> [1,2]
又无情的携带[1,2]进入函数，但此时函数首先检测到长度够了，于是退出。
于是执行
`path.append(i)` 
`[1] ----> [1,2]`
这一环节的pop
[1,2] ---->[1]
由于for循环，接下来该[1,3]了

![[回溯part01-1749027249972.jpeg]]
## 小细节
1.`result.append(path[:])` 和 `result.append(path)` 的结果不同
1. **`result.append(path[:])`**
    
    - `path[:]` 创建了 `path` 列表的一个**浅拷贝**（即一个新的列表，内容和 `path` 相同）。
    - 这样即使后续 `path` 被修改（比如 `path.pop()`），`result` 中已经保存的拷贝不会受到影响。
    - 这是正确的做法，因为我们需要保存当前状态的组合。
2. **`result.append(path)`**
    
    - 这里直接追加了 `path` 的**引用**（而不是拷贝）。
    - 后续对 `path` 的任何修改（比如 `path.pop()`）都会影响 `result` 中已经存储的列表，因为它们指向同一个对象。
    - 最终 `result` 中的所有组合都会是空列表（因为回溯结束后 `path` 会被清空）

2.我们可以将
 for i in range(startIndex, n + 1):
优化为
 for i in range(startIndex, n - (k - len(path)) + 2)
 假设我们要从 `1` 到 `n` 中选出 `k` 个数的组合，而当前已经选了 `len(path)` 个数，还需要选 `k - len(path)` 个数。
**如果剩余可选数字不够 `k - len(path)` 个，就没必要继续递归了**
1. **假设以当前的path，剩余需要选的数字个数**：`remaining = k - len(path)`
2. **当前循环中最大可选起始点？**
    - 共需要remaining个 我们现在思考的是，避免我们八九需要3个，但起始点后面只有2个数，这样的起始点情况。
    - 所以`i` 的最大可能值是 `n - remaining + 1)`，比如n是5，需要一个的话，那最大起始点是最后一个数‘n’即‘5也没问题，此时是n - 1 + 1，比如需要2个的话，最大起始点就应该是4了，而不是‘n’即5
    - 由于 `range` 是左闭右开区间，所以循环的终止条件是 `n - (k - len(path)) + 2`
### **再次举例说明**

假设 `n=4, k=2`，当前 `path=[]`（还没选任何数）：

- `remaining = k - len(path) = 2`
- 最大可选起始点：`n - (k - len(path)) + 1 = 4 - 2 + 1 = 3`
- 所以 `i` 的范围是 `1` 到 `3`（因为 `range` 是 `[start, end)`，所以 `range(1, 4)` 变成 `range(1, 3 + 1)`）。
    - 如果 `i=4`，后面没有足够的数字可以选（因为还需要 `1` 个数字，但 `4` 后面没有数字了），所以不需要考虑 `i=4`
### 优化效果
看这个n=4， k=4的输入例子
所有的红叉，如果按不优化的算法，都无法触发if len(path) == k这个条件，从而一直pop到0.所以干脆就不要经历红叉![[回溯part01-1749028802225.jpeg]]
# 216 组合总和 III
找出所有相加之和为 `n` 的 `k` 个数的组合，且满足下列条件：

- 只使用数字1到9
- 每个数字 **最多使用一次** 

返回 _所有可能的有效组合的列表_ 。该列表不能包含相同的组合两次，组合可以以任何顺序返回。
## 题解
这为什么也能用回溯？
实质上本题是给你【1，2，3，4，5，6，7，8，9】 
最简单的思路是不是k层循环，不断加数看哪个组合等于n呀？有这种简单的循环思路就能转化成回溯（性质是一样的）

```python
def combinationSum3(self, k: int, n: int) -> List[List[int]]:

        result = []

        path = []

        self.backtrace(k, n, 1, 0, path, result)

        return result

    def backtrace(self, k, n, start, current_sum, path, result):

        if current_sum > n:

            return

        if len(path) == k:

            if current_sum == n:

                result.append(path[:])

            return

        for i in range(start, 9 - (k - len(path)) + 2):

            path.append(i)

            current_sum += i

            self.backtrace(k,n,i+1,current_sum,path,result)

            current_sum -= i

            path.pop()

```
## 小细节
可以说代码有两次剪枝（即优化冗余）的地方
for i in range(start, 9 - (k - len(path)) + 2)仍然是像上一题，在长度上的剪枝
还有一处是
if current_sum > n:
            return
 诶对，这其实是剪枝，如果没有这处代码程序仍然能返回正确结果（可以自己调试），但是程序会在有些不必要的地方苦恼，比如n=2，如果没这处代码它会拿3开始与别人加，与4加与5加，哎呀怎么就是加起来不等于n呢？最后for循环用完了，只能不断pop，最后pop到【】   
# 17 电话号码的字母组合
给定一个仅包含数字 `2-9` 的字符串，返回所有它能表示的字母组合。答案可以按 **任意顺序** 返回。

给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。![[回溯part01-1749052684272.jpeg]]
## 题解
其实这一题递归味很弄，回溯的那个“pop”，即回溯到上一把重新抉择没有在本题体现
```python
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        
        phone_map = {
            '2': 'abc',
            '3': 'def',
            '4': 'ghi',
            '5': 'jkl',
            '6': 'mno',
            '7': 'pqrs',
            '8': 'tuv',
            '9': 'wxyz'
        }
        
        res = []
        
        def backtrack(index, current):
            if index == len(digits):
                res.append(current)
                return
            
            for char in phone_map[digits[index]]:
                backtrack(index + 1, current + char)
        
        backtrack(0, '')
        return res
```