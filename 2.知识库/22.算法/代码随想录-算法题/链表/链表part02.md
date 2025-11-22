
# 24 两两交换节点
每次交换，实际上用三个节点！第一个节点位置不变 第二、第三位置改变
举个例子：
输入：head = [1,2,3,4]
第一个循环：dummy、1、2 三个节点互相操作，
第二个循环，1（因为被交换过了）、3、4 三个节点互相操作，1位置不变
最后是2，1，4，3

为什么不能return head？
因为head除了在dummy_head.next = head出现，再没有改动过了
head始终指代的最开始的第一个数
举个例子：
输入：head = [1,2,3,4]
- 原始头节点是 `1`
- 交换后变成 `[2,1,3,4]`，新的头节点变成了 `2`

如果你在函数最后返回了 `head`，那么结果就是错的，它仍然指向 `1`，而实际上正确的头节点已经变成了 `2`。


```python
class Solution:

    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:

        dummy_head = ListNode()

        dummy_head.next = head

        cur = dummy_head

        while cur.next and cur.next.next:

  

            first = cur.next

            second = cur.next.next

            third = second.next

  

            cur.next = second

  

            second.next = first

  

            first.next = third

  

            cur = first

        return dummy_head.next

```
递归版本
1. 定义宏观功能：给一个头节点，返回一个已经两两交换的链表的头节点
2. 最简单的输入是怎样： 空，或者只有一个节点，之间返回本身
3. 视角拉近：考虑把谁送进递归函数里，自己又怎么处理自己。显然是把next的next送进函数。自己的话，写个交换逻辑。

```python
def swap(head):
	if not head or not head.next:
		return head
		
	first = head
	second = head.next
	
	second.next = head
	first.next = swap(head.next.next)
	
	return second
	


```

# 19 删除链表倒数第n个
快慢指针，比较简单

```python
class Solution:

    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:

        dummy_head = ListNode(next = head)

        fast = slow = dummy_head

        for _ in range(n):

            if fast:

                fast = fast.next

  

        while fast.next:

            slow = slow.next

            fast = fast.next

  

        slow.next = slow.next.next

  

        return dummy_head.next

```
# 0207 . 链表相交

## 题目描述
给你两个单链表的头节点 `headA` 和 `headB` ，请你找出并返回两个单链表相交的起始节点。如果两个链表没有交点，返回 `null` 。
## 解法一
要看懂题目，相交指的是，公共部分！求的是相交的起始节点
那比如A有5个节点，B有6个节点，那相交起始点假如是A的倒数第三个，那一定也是B的倒数第三个，A和B的倒数三个节点都一样！  
那么此时，对于A，相交节点前有2个，对于B，相交节点前有3个。那我们可以从B的第二个节点，A的第一个节点，两个指针同时遍历！![[链表part02-1747490945049.jpeg]]
也就是a1、b2-----》 a2、b3------》c1、c1，发现相交，返回
代码很简单呀，我们算出链表长度差值就好
## 解法二
这个题解太优雅了！ 
借用一下qwen3的解释
假设：

- 链表 `headA` 的长度为 `L1 + C`，其中 `C` 是公共部分（相交后的部分）。
- 链表 `headB` 的长度为 `L2 + C`，其中 `C` 是公共部分。
- 相交的起始节点距离 `headA` 为 `L1`，距离 `headB` 为 `L2`。

#### (1) **双指针遍历路径**

- 指针 `A` 的路径：先遍历 `headA` 到末尾，然后跳到 `headB` 继续遍历。
    - 总路径长度：`L1 + C + L2`。
- 指针 `B` 的路径：先遍历 `headB` 到末尾，然后跳到 `headA` 继续遍历。
    - 总路径长度：`L2 + C + L1`。

由于 `L1 + C + L2 = L2 + C + L1`，两个指针的总路径长度是一致的。

#### (2) **相遇点的意义**

- 当两个链表相交时，两个指针在各自的路径中会经过相同的总长度，因此它们会在相交点相遇。
- 如果没有相交，两个指针最终会同时到达空节点（`None`），从而退出循环。

我们看上面的例子!![[链表part02-1747491639545.jpeg]]
A从a1走，走完c3，跳到b1开始走，走到c1 是不是所有节点遍历了一遍
B从b1走，走完c3，跳到a1开始走，走到c1是不是所有节点遍历一遍，

```python
A: a1 → a2 → a3 → c1 → c2
B:           b1 → c1 → c2
```
A 的长度是 5，B 的长度是 3
- A 走完后跳去 B 的头（b1），B 走完后跳去 A 的头（a1）
- 最终两人会在 c1 处相遇

代码：

```python
  def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:

        A, B = headA, headB

        while A != B:

            A = A.next if A else headB

            B = B.next if B else headA

        return A
```
相比第一个解法还要用循环算链表长度、移动指针，这里5行代码实在优雅！
# 142 环形链表II

## 题目描述
给定一个链表的头节点  `head` ，返回链表开始入环的第一个节点。 _如果链表无环，则返回 `null`。_

如果链表中有某个节点，可以通过连续跟踪 `next` 指针再次到达，则链表中存在环。 为了表示给定链表中的环，评测系统内部使用整数 `pos` 来表示链表尾连接到链表中的位置（**索引从 0 开始**）。如果 `pos` 是 `-1`，则在该链表中没有环。**注意：`pos` 不作为参数进行传递**，仅仅是为了标识链表的实际情况。

**不允许修改** 链表。
## 解题之前需要掌握的
- 快慢指针可以识别是否有环：假如有环，快指针一直在走两步，慢指针走一步，无论路程是怎么样的，他俩一定相遇，相遇位置和路程有关。好比两个同学一直在操场跑圈，一个快一点一个慢点，但一定能相遇
- 相遇位置的特殊性：相遇位置有哪些数学等式？
      - ![[链表part02-1747494142054.jpeg]]
     
     -  慢指针步数b，快指针2b，2b-b = kc  也就是相遇的特殊性为：慢指针走的步数，就是k个环长
     - 环内的步数，为kc - a
     - 以上两个数学公式，都不是考理解的！而是纯粹的演算
     - 接着就简单了，环内步数是kc-a，那走a步不就kc步了？不就到环入口了？ 那从相遇开始，让slow走a就好了，至于a是几步，让head来当导盲犬！

```python
 def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:

        slow = fast =head

        while fast and fast.next:

            slow = slow.next

            fast = fast.next.next

            if fast is slow:

                while slow is not head:

                    slow = slow.next

                    head = head.next

                return slow

        return None

```

下面的集合方法不需要任何数学推算，很简单，一眼看懂。应该是python独一份了，哈哈

```python

    def detectCycle(self, head: ListNode) -> ListNode:
        visited = set()
        
        while head:
            if head in visited:
                return head
            visited.add(head)
            head = head.next
        
        return None
```



