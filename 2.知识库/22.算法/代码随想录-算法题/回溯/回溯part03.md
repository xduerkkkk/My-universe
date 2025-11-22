# 93.复原IP地址
给定一个只包含数字的字符串，复原它并返回所有可能的 IP 地址格式。

有效的 IP 地址 正好由四个整数（每个整数位于 0 到 255 之间组成，且不能含有前导 0），整数之间用 '.' 分隔。

例如："0.1.2.201" 和 "192.168.1.1" 是 有效的 IP 地址，但是 "0.011.255.245"、"192.168.1.312" 和 "192.168@1.1" 是 无效的 IP 地址。

示例 1：

- 输入：s = "25525511135"
- 输出：["255.255.11.135","255.255.111.35"]
## 题解
切割问题中，终止条件都是
```
 if startIndex == len(s)
```
也就是成功遍历到最后一个了

```python
class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        result = []
        self.backtracking(s, 0, [], result)
        return result
    
    def backtracking(self, s, startIndex, path, result):
        if startIndex == len(s):
            result.append('.'.join(path[:]))
            return
        
        for i in range(startIndex, min(startIndex+3, len(s))):
            # 如果 i 往后遍历了，并且当前地址的第一个元素是 0 ，就直接退出
            if i > startIndex and s[startIndex] == '0':
                break
            # 比如 s 长度为 5，当前遍历到 i = 3 这个元素
            # 因为还没有执行任何操作，所以此时剩下的元素数量就是 5 - 3 = 2 ，即包括当前的 i 本身
            # path 里面是当前包含的子串，所以有几个元素就表示储存了几个地址
            # 所以 (4 - len(path)) * 3 表示当前路径至多能存放的元素个数
            # 4 - len(path) 表示至少要存放的元素个数
            if (4 - len(path)) * 3 < len(s) - i or 4 - len(path) > len(s) - i:
                break
            if i - startIndex == 2:
                if not int(s[startIndex:i+1]) <= 255:
                    break
            path.append(s[startIndex:i+1])
            self.backtracking(s, i+1, path, result)
            path.pop()
```
# 78 子集
给定一组不含重复元素的整数数组 nums，返回该数组所有可能的子集（幂集）。

说明：解集不能包含重复的子集。

示例: 输入: nums = [1,2,3] 输出: [ [3],   [1],   [2],   [1,2,3],   [1,3],   [2,3],   [1,2],   []
## 题解
`没想到自己一遍过了
`记得大一初次见面折磨我3个小时还做不出来抄的AI，系统刷题真的有必要`
本题中的回溯逻辑部分，需要注意的点在于
一来就result.append(path[:])，每一层都需要被记录
以及return是再所有逻辑实现完直接return，不用任何条件判断（所以也可以把这个return去掉，for循环后函数会自动结束）
![[回溯part03-1749186000389.jpeg]]
```python
class Solution:

    def subsets(self, nums: List[int]) -> List[List[int]]:

        result = []

        path = []

        def backtrace(nums,start_index,path,result):

            result.append(path[:])

  

            for i in range(start_index,len(nums)):

                path.append(nums[i])

                backtrace(nums,i+1,path,result)

                path.pop()

  

            return

        backtrace(nums,0,path,result)

        return result

```
# 90.子集II
给定一个可能包含重复元素的整数数组 nums，返回该数组所有可能的子集（幂集）。

说明：解集不能包含重复的子集。

示例:

- 输入: [1,2,2]
- 输出: [ [2], [1], [1,2,2], [2,2], [1,2], [] ]
## 题解
本题的考点是去重
在研究如何去重之前，我的理解是需要懂回溯过程的“纵向遍历”和“横向遍历”都是哪些部分
显然，这个树的宽度是横向遍历，深度是纵向遍历（我不会说了个废话吧）
![[回溯part03-1749224996926.jpeg]]
我们拿代码来说
不断递归，触发backtrace，
第一次self.backtracking(nums, 0, path, result)后
一路沿着树的最左侧走到{1,2,2}，这就是纵向遍历
{1,2,2}一路回溯到，pop到{1}，pop到{}
开始执行
for i in range(start_index,len(nums)):
变为{2}，就是横向遍历

那去重在哪块呢？
加入集合为{1,1,2,3,4,5}
横向遍历第一个1和横向遍历第二个1，结果是不是显然会重复？
所以去重在横向这里

两个方法
在递归函数中，直接于for循环前加入
uset = set()
```python
 def backtracking(self, nums, startIndex, path, result):
        result.append(path[:])  # 收集子集
        uset = set()
        for i in range(startIndex, len(nums)):
            if nums[i] in uset:
                continue
            uset.add(nums[i])
            path.append(nums[i])
            self.backtracking(nums, i + 1, path, result)
            path.pop()
```
或直接加判断逻辑

```python
for i in range(startIndex, len(nums)):
            # 而我们要对同一树层使用过的元素进行跳过
            if i > startIndex and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            self.backtracking(nums, i + 1, path, result)
            path.pop()
```

当然，去重一般都是要**排序**的哦