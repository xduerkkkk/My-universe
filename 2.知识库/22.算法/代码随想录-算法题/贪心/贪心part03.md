# 134 加油站
在一条环路上有 `n` 个加油站，其中第 `i` 个加油站有汽油 `gas[i]` 升。

你有一辆油箱容量无限的的汽车，从第 `i` 个加油站开往第 `i+1` 个加油站需要消耗汽油 `cost[i]` 升。你从其中的一个加油站出发，开始时油箱为空。

给定两个整数数组 `gas` 和 `cost` ，如果你可以按顺序绕环路行驶一周，则返回出发时加油站的编号，否则返回 `-1` 。如果存在解，则 **保证** 它是 **唯一** 的。

**示例 1:**

**输入:** gas = [1,2,3,4,5], cost = [3,4,5,1,2]
**输出:** 3
**解释:**
从 3 号加油站(索引为 3 处)出发，可获得 4 升汽油。此时油箱有 = 0 + 4 = 4 升汽油
开往 4 号加油站，此时油箱有 4 - 1 + 5 = 8 升汽油
开往 0 号加油站，此时油箱有 8 - 2 + 1 = 7 升汽油
开往 1 号加油站，此时油箱有 7 - 3 + 2 = 6 升汽油
开往 2 号加油站，此时油箱有 6 - 4 + 3 = 5 升汽油
开往 3 号加油站，你需要消耗 5 升汽油，正好足够你返回到 3 号加油站。
因此，3 可为起始索引。
## 题解
这是二刷本题哈
- 首先，暴力模拟可以做，每个点都去试一次。但题解就不说了。
- 为啥只有一个解？啊是因为答案案例就这么设计的，我们自己写例子可以写出有两个解的，甚至每个加油站都能出行的例子


核心只在一句话
i从0开始累加rest[i]，和记为totalsum，一旦totalSum小于零，说明[0, i]区间都不能作为起始位置，因为这个区间选择任何一个位置作为起点，到i这里都会断油
为什么？ 为什么出现累加和小于0时，从0到这个i中间任何一个地方都不能当起点？
- 数学法： 假设`curSum` 在 `i` 处首次 `< 0`。如果存在某个 `k ∈ [0, i]` 可以作为起点，那么从 `k` 出发到 `i` 的油量必须满足大于0！就是`[k,i]`这一段cursum>0      但是`[0,i]`cursum<0，故而 `[0,k]`应该小于0，这与`curSum` 在 `i` 处首次 `< 0`矛盾
- 通俗理解：
	- **局部负债拖累全局**： 一段路的净消耗为负，就像“团队中有几个拖后腿的成员”，无论怎么调整队形，只要包含他们，整体就会失败。
	- **唯一希望是砍掉负债段**： 直接跳过这段，从下一个“可能靠谱”的起点重新尝试。

```python
class Solution:

    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:

        cur_sum = 0

        min_sum = 0

        ans = 0

        for i in range(len(gas)):

            cur_sum += gas[i] - cost[i]

            if cur_sum < min_sum:

                min_sum = cur_sum

                ans = i + 1

        if cur_sum < 0 :

            return -1

        return ans

```
# &135 分发糖果
`n` 个孩子站成一排。给你一个整数数组 `ratings` 表示每个孩子的评分。

你需要按照以下要求，给这些孩子分发糖果：

- 每个孩子至少分配到 `1` 个糖果。
- 相邻两个孩子评分更高的孩子会获得更多的糖果。

请你给每个孩子分发糖果，计算并返回需要准备的 **最少糖果数目**
## 题解
这道题....我还没有悟出来为什么左边遍历一次，右边遍历一次，就能得到最终的准确结果，时间不太够了，先标记一下
```python
def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        candies = [1] * n
        
        # Forward pass: handle cases where right rating is higher than left
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1
        
        # Backward pass: handle cases where left rating is higher than right
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)
        
        return sum(candies)
```
# 860 柠檬水找零
在柠檬水摊上，每一杯柠檬水的售价为 `5` 美元。顾客排队购买你的产品，（按账单 `bills` 支付的顺序）一次购买一杯。

每位顾客只买一杯柠檬水，然后向你付 `5` 美元、`10` 美元或 `20` 美元。你必须给每个顾客正确找零，也就是说净交易是每位顾客向你支付 `5` 美元。

注意，一开始你手头没有任何零钱。

给你一个整数数组 `bills` ，其中 `bills[i]` 是第 `i` 位顾客付的账。如果你能给每位顾客正确找零，返回 `true` ，否则返回 `false` 。
## 题解
这里的贪心，就是优先找10、20这种难以当零钱的（相比5元来说，5元很灵活，10、20太死板）
```python
def lemonadeChange(self, bills: List[int]) -> bool:
        five = 0
        ten = 0
        twenty = 0
        
        for bill in bills:
            # 情况一：收到5美元
            if bill == 5:
                five += 1
            
            # 情况二：收到10美元
            if bill == 10:
                if five <= 0:
                    return False
                ten += 1
                five -= 1
            
            # 情况三：收到20美元
            if bill == 20:
                # 先尝试使用10美元和5美元找零
                if five > 0 and ten > 0:
                    five -= 1
                    ten -= 1
                    #twenty += 1
                # 如果无法使用10美元找零，则尝试使用三张5美元找零
                elif five >= 3:
                    five -= 3
                    #twenty += 1
                else:
                    return False
        
        return True
```