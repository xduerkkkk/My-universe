#  接雨水

[力扣题目链接(opens new window)](https://leetcode.cn/problems/trapping-rain-water/)

给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。

示例 1：

输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]
- 输出：6
- 解释：上面是由数组 [0,1,0,2,1,0,1,3,2,1,2,1] 表示的高度图，在这种情况下，可以接 6 个单位的雨水（蓝色部分表示雨水）。

示例 2：

- 输入：height = [4,2,0,3,2,5]
- 输出：9

![[单调栈part02-1752060646827.jpeg]]
## 题解
雨水是由凹槽接的，凹槽怎么来的呢？是三个及以上高度一定不完全相同的柱子，组成的。有的柱子啊，上面就放的雨水，是凹槽的底座。有的柱子呢，是拦着雨水，是凹槽的高部。
那计算机怎么知道柱子是接着雨水还是拦着雨水呢？
一个柱子一个柱子的看呗。 遍历到该柱子，从左边，从右边，都去看看，两边有没有比该柱子更高的柱子，如果有，此柱子一定就是凹槽的底部。 这个思想就是双指针实现的。

但本文是单调栈专题，回顾一下单调栈，要让`stack[-1]` （即栈头）始终最小，且每个元素都要加入到栈里。那想如果新元素比`stack[-1]` 大，且由于栈的特性新元素必须是栈头，即`stack[-1` 那就要把原先的栈头踢掉，一直踢，直到这个新元素能符合这个规则为之（栈头最小），即自己最小。
想象上面流程，栈，从`stack[0] 到 stacl[-1]` 势必是递减的序列，每次添加新元素时都要踢人，确保加到栈头的新元素是最小的元素，故命名为单调栈。

注意，栈里面可以是元素大小，但几乎每个题都要用到元素所在数组的索引，所以干脆栈里面添加索引，这样元素位置和元素大小都能定位到。

![[单调栈part02-1752061334457.jpeg]]

只要有更高的出现 就一定要弹，每弹一次都要接一次雨水，不像传统的单调栈一弹弹到底
![[单调栈part02-1752063115739.jpeg]]
注意，黑色的是“0”
![[单调栈part02-1752063131705.jpeg]]
此时出现了1，那要把这个0踢了呀。  
只要出现踢人动作，我们就进行接雨水
我们会发现这个雨水所在凹槽的三部分，分别来自被踢者左侧，被踢者，和踢人者
雨水的宽度，就来自于踢人者和被踢者左侧的距离
即
```python
# 雨水高度是 min(凹槽左侧高度, 凹槽右侧高度) - 凹槽底部高度

h = min(height[stack[-1]], height[i]) - height[mid_height]

# 雨水宽度是 凹槽右侧的下标 - 凹槽左侧的下标 - 1

w = i - stack[-1] - 1

```

注意下面这个情况，3进来，会弹走1，
按逻辑来说一弹到人我们就接水，但显然我们应该是3与2接水啊，
这样弹1，stack【-1】仍然是-1，3与1接不对啊？
注意雨水高度是 min(凹槽左侧高度, 凹槽右侧高度) - 凹槽底部高度  
`h = min(height[stack[-1]], height[i]) - height[mid_height]` 所以此时接的雨水是0
继续弹，就能3与2接雨水了

![[单调栈part02-1752064307016.jpeg]]

完整代码
```python
 def trap(self, height: List[int]) -> int:

        stack = []

        ans = 0

  

        for i in range(len(height)):

            while stack and height[i] > height[stack[-1]]:              

                mid = stack.pop()

                if stack:

                    rain = (min(height[stack[-1]],height[i]) - height[mid]) *(i-stack[-1]-1)

                    ans += rain

            stack.append(i)

        return ans

```
那实际上，我们应该把相同元素合并了，可以做这个合并逻辑
这样最清晰![[单调栈part02-1752064421652.jpeg]]![[单调栈part02-1752064424859.jpeg]]
如果要足够清晰，不出错，那代码逻辑如下
```python
def trap(self, height: List[int]) -> int:
        # 单调栈
        '''
        单调栈是按照 行 的方向来计算雨水
        从栈顶到栈底的顺序：从小到大
        通过三个元素来接水：栈顶，栈顶的下一个元素，以及即将入栈的元素
        雨水高度是 min(凹槽左边高度, 凹槽右边高度) - 凹槽底部高度
        雨水的宽度是 凹槽右边的下标 - 凹槽左边的下标 - 1（因为只求中间宽度）
        '''
        # stack储存index，用于计算对应的柱子高度
        stack = [0]
        result = 0
        for i in range(1, len(height)):
            # 情况一
            if height[i] < height[stack[-1]]:
                stack.append(i)

            # 情况二
            # 当当前柱子高度和栈顶一致时，左边的一个是不可能存放雨水的，所以保留右侧新柱子
            # 需要使用最右边的柱子来计算宽度
            elif height[i] == height[stack[-1]]:
                stack.pop()
                stack.append(i)

            # 情况三
            else:
                # 抛出所有较低的柱子
                while stack and height[i] > height[stack[-1]]:
                    # 栈顶就是中间的柱子：储水槽，就是凹槽的地步
                    mid_height = height[stack[-1]]
                    stack.pop()
                    if stack:
                        right_height = height[i]
                        left_height = height[stack[-1]]
                        # 两侧的较矮一方的高度 - 凹槽底部高度
                        h = min(right_height, left_height) - mid_height
                        # 凹槽右侧下标 - 凹槽左侧下标 - 1: 只求中间宽度
                        w = i - stack[-1] - 1
                        # 体积：高乘宽
                        result += h * w
                stack.append(i)
        return result
```
# 84.柱状图中最大的矩形

[力扣题目链接(opens new window)](https://leetcode.cn/problems/largest-rectangle-in-histogram/)

给定 n 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1 。

求在该柱状图中，能够勾勒出来的矩形的最大面积

![[单调栈part02-1752064536233.jpeg]]
![[单调栈part02-1752064581061.jpeg]]

## 题解
与接雨水对照看即可
本题要找的是每个柱子左边和右边第一个比它小的柱子

不要想象如题示的图片一样，直接画

下面给出图片中矩阵10的由来

| 索引      | 大小      | 动作                | stack          | answer                                                               |
| ------- | ------- | ----------------- | -------------- | -------------------------------------------------------------------- |
| 4       | 6       | 6 > 栈顶高度5，索引4入栈   | `[0, 2, 3, 4]` | -                                                                    |
| ​**5**​ | ​**2**​ | 2 < 栈顶高度6 → 弹出索引4 | `[0, 2, 3]`    | ​**面积2**​：高度=`heights[4]=6`，宽度=`i(5)-新栈顶(3)-1=1` → `6×1=6`           |
|         |         | 2 < 栈顶高度5 → 弹出索引3 | `[0, 2]`       | ​**面积3**​：高度=`heights[3]=5`，宽度=`i(5)-新栈顶(2)-1=2` → `5×2=10`（**最大值**） |


重点理解：
- 因为左右两端也能算成答案，左右两端要加一个哨兵0，为什么？

那这次来细节版
```python
 def largestRectangleArea(self, heights: List[int]) -> int:
        # Monotonic Stack
        '''
        找每个柱子左右侧的第一个高度值小于该柱子的柱子
        单调栈：栈顶到栈底：从大到小（每插入一个新的小数值时，都要弹出先前的大数值）
        栈顶，栈顶的下一个元素，即将入栈的元素：这三个元素组成了最大面积的高度和宽度
        情况一：当前遍历的元素heights[i]大于栈顶元素的情况
        情况二：当前遍历的元素heights[i]等于栈顶元素的情况
        情况三：当前遍历的元素heights[i]小于栈顶元素的情况
        '''

        # 输入数组首尾各补上一个0（与42.接雨水不同的是，本题原首尾的两个柱子可以作为核心柱进行最大面积尝试
        heights.insert(0, 0)
        heights.append(0)
        stack = [0]
        result = 0
        for i in range(1, len(heights)):
            # 情况一
            if heights[i] > heights[stack[-1]]:
                stack.append(i)
            # 情况二
            elif heights[i] == heights[stack[-1]]:
                stack.pop()
                stack.append(i)
            # 情况三
            else:
                # 抛出所有较高的柱子
                while stack and heights[i] < heights[stack[-1]]:
                    # 栈顶就是中间的柱子，主心骨
                    mid_index = stack[-1]
                    stack.pop()
                    if stack:
                        left_index = stack[-1]
                        right_index = i
                        width = right_index - left_index - 1
                        height = heights[mid_index]
                        result = max(result, width * height)
                stack.append(i)
        return result
```