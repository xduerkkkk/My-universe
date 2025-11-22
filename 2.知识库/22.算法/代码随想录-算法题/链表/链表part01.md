# 203移除链表元素
### 题目描述
给你一个链表的头节点 `head` 和一个整数 `val` ，请你删除链表中所有满足 `Node.val == val` 的节点，并返回 **新的头节点** 。

### 解法

想要一个循环解决的话
需要掌握“虚拟头节点”
但是再给链表前加一个节点，虚拟头节点,只占位，就能一路“next”了
```python
def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:

        dummy = Listnode(next=head)
        current = dummy
        while current!=None:
	        if current.next.val == val:
		        current.next = current.next.next
		    else:
				current = current.next
		return dummy.next

```


注意

```

	        if current.next.val == val:
		        current.next = current.next.next
		    else:
				current = current.next
		
```
与

``` 
			if current.next.val == val:
			        current.next = current.next.next
			    
			current = current.next
			

```
效果完全不同！ 
当判断要删除节点时，不应该删一个就继续往下走。
有可能要进行连续删除！所以应该有‘else’


更优雅的解法，递归：

```python
    def removeElements(self, head: ListNode, val: int) -> ListNode:
        if not head:
	        return None
	    head.next = removeElements(head.next)
	    
	    if head.val == val:
		    return head.next
		else :
			return head
		
		# return head.next if head.val == val else head

```
实在太优雅了，只是空间复杂度变为n （上个方法是1）

# 707手撕链表


```python
def get(self, index: int) -> int:

        #边界检查

        if index<0 or index >= self.size :#所以说，得有长度嘛

            return -1

        current = self.dummy_head

        for i in range(1,index+1):

            current = current.next

        return current.val

```
错误：
```
Node(val).next = current.next # 错误！此节点未被引用
current.next = Node(val) # 新建另一个节点，next默认None
```

```python
new_node = Node(val)
new_node.next = current.next 
current.next = new_node

```
记录第一次不优雅的单链表：

```python
class Node:

    def __init__(self,val):

        self.val = val

        self.next = None

  

class MyLinkedList:

  

    def __init__(self):

        #没有传val参

        self.size = 0

        self.dummy_head = Node(0)

  

    def get(self, index: int) -> int:

        #边界检查

        if index<0 or index >= self.size :#所以说，得有长度嘛

            return -1

        current = self.dummy_head.next

        for _ in range(index):

            current = current.next

        return current.val

  

    def addAtHead(self, val: int) -> None:

        p = Node(val)

        p.next = self.dummy_head.next

        self.dummy_head.next = p

        self.size += 1

  

    def addAtTail(self, val: int) -> None:

        current = self.dummy_head

        for i in range(self.size):

            current = current.next

        current.next = Node(val)

        self.size += 1

  

    def addAtIndex(self, index: int, val: int) -> None:

        if index <0 or index > self.size:

            return

  

        current = self.dummy_head

        for i in range(index):

            current = current.next

        new_node = Node(val)

        new_node.next = current.next

        current.next = new_node

        self.size += 1

  

    def deleteAtIndex(self, index: int) -> None:

        if index <0 or index >= self.size:

            return

  

        current = self.dummy_head

        for i in range(index):

            current = current.next

        current.next = current.next.next

        self.size -= 1
```


# 206 反转链表
比较简单，双指针操作。
值得注意的是，pre的初始化，初始化成None即可
在while循环里会再次定义
优雅：

```python
class Solution:

    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
	    
	    pre = None
	    cur = head
	    
	    
	    while cur and cur.next:
		    nxt = cur.next
		    cur.next = pre
		    pre = cur
		    cur = nxt
		    
		 return pre
			    	    

```
递归版
1. 我函数的能力是反转head后面的列表
2. 如果只有一个或者没有 return head
3. 自己的话，我应该跟着反向过的链表


```python
def reverse(head):
	if not head or not head.next:
		return head
	head.next.next = head
	head.next=None
	
	retur
	

```

# 反转链表II
采用头插法

```python
 dummy = ListNode(next=head)

        pre = dummy

  

        for _ in range(left-1):

            pre = pre.next

        cur = pre.next

  

        for _ in range(right-left):

            nxt = cur.next

            cur.next = nxt.next

            nxt.next = pre.next

            pre.next = nxt

  

        return dummy.next
```
# k个一组反转链表

朴素版

```python
class Solution:

    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:

        dummy = ListNode(next=head)

        pre = dummy

        cur = pre.next

        end = pre

        while True:

            for _ in range(k):

                end = end.next

                if not end:

                    return dummy.next

            for _ in range(k-1):

                nxt = cur.next

                cur.next = nxt.next

                nxt.next = pre.next

                pre.next = nxt

            pre = cur

            cur = pre.next

            end = pre

  

        return dummy.next
```


调用函数版本


```python
class Solution:
    # 这是一个辅助函数，就是你之前写的标准反转链表
    # 把它独立出来，会让主逻辑非常清晰
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pre = None
        cur = head
        while cur:
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt
        return pre

    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        # 1. 地基
        dummy = ListNode(next=head)
        pre = dummy

        # 2. 流水线主循环
        while True:
            # 3. 第一站：分组，找到 end
            end = pre
            for _ in range(k):
                end = end.next
                if not end:
                    # 剩余节点不足 k 个，直接返回
                    return dummy.next
            
            # 4. 第二站：切割并反转
            # 记录关键节点
            start = pre.next
            next_group_head = end.next
            
            # 切割
            end.next = None
            
            # 反转，并把 pre 连接到反转后的新头上
            pre.next = self.reverseList(start)
            
            # 5. 第三站：缝合
            # 反转后的尾巴(start)连接到下一组的头上
            start.next = next_group_head
            
            # 6. 为下一轮做准备
            # 更新 pre，移动到下一组的前面
            pre = start
```
