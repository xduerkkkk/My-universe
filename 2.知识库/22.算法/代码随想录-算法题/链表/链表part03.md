# [138. 随机链表的复制](https://leetcode.cn/problems/copy-list-with-random-pointer/)

给你一个长度为 `n` 的链表，每个节点包含一个额外增加的随机指针 `random` ，该指针可以指向链表中的任何节点或空节点。

构造这个链表的 **[深拷贝](https://baike.baidu.com/item/%E6%B7%B1%E6%8B%B7%E8%B4%9D/22785317?fr=aladdin)**。 深拷贝应该正好由 `n` 个 **全新** 节点组成，其中每个新节点的值都设为其对应的原节点的值。新节点的 `next` 指针和 `random` 指针也都应指向复制链表中的新节点，并使原链表和复制链表中的这些指针能够表示相同的链表状态。**复制链表中的指针都不应指向原链表中的节点** 。

例如，如果原链表中有 `X` 和 `Y` 两个节点，其中 `X.random --> Y` 。那么在复制链表中对应的两个节点 `x` 和 `y` ，同样有 `x.random --> y` 。

返回复制链表的头节点。

用一个由 `n` 个节点组成的链表来表示输入/输出中的链表。每个节点用一个 `[val, random_index]` 表示：

- `val`：一个表示 `Node.val` 的整数。
- `random_index`：随机指针指向的节点索引（范围从 `0` 到 `n-1`）；如果不指向任何节点，则为  `null` 。

你的代码 **只** 接受原链表的头节点 `head` 作为传入参数。

**示例 1：**

![](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2020/01/09/e1.png)

**输入：**head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
**输出：**[[7,null],[13,0],[11,4],[10,2],[1,0]]

# [146. LRU 缓存](https://leetcode.cn/problems/lru-cache/)

已解答

中等

相关标签

![premium lock icon](https://static.leetcode.cn/cn-frontendx-assets/production/_next/static/images/lock-a6627e2c7fa0ce8bc117c109fb4e567d.svg)相关企业

请你设计并实现一个满足  [LRU (最近最少使用) 缓存](https://baike.baidu.com/item/LRU) 约束的数据结构。

```python
class LRUCache:

    # Node 类的定义非常完美

    class DLinkedNode:

        def __init__(self, key=0, value=0):

            self.key = key

            self.value = value

            self.prev = None

            self.next = None

  

    # __init__ 的设计也非常完美

    def __init__(self, capacity: int):

        self.cache = {}

        self.head = self.DLinkedNode() # 虚拟头节点

        self.tail = self.DLinkedNode() # 虚拟尾节点

        self.head.next = self.tail

        self.tail.prev = self.head

        self.capacity = capacity

        self.size = 0

  

    # --- 抽离出来的辅助函数 ---

    def _move_to_head(self, node):

        # 1. 先将 node 从原位置断开

        node.prev.next = node.next

        node.next.prev = node.prev

        # 2. 再将 node 插入到虚拟头节点后

        node.next = self.head.next

        node.prev = self.head

        self.head.next.prev = node

        self.head.next = node

  

    def _add_to_head(self, node):

        # (这是一个更简单的版本，只负责添加)

        node.next = self.head.next

        node.prev = self.head

        self.head.next.prev = node

        self.head.next = node

  

    def _remove_node(self, node):

        # 通用的节点删除函数

        node.prev.next = node.next

        node.next.prev = node.prev

  

    def _remove_tail(self):

        # 删除虚拟尾节点的前一个节点

        removed_node = self.tail.prev

        self._remove_node(removed_node)

        return removed_node

  

    # --- 核心的 get 和 put 方法 ---

  

    def get(self, key: int) -> int:

        if key not in self.cache:

            return -1

        # 如果 key 存在

        node = self.cache[key]

        # 将其移动到链表头部（表示最近使用）

        self._move_to_head(node)

        return node.value

  

    def put(self, key: int, value: int) -> None:

        if key in self.cache:

            # 如果 key 已存在，更新 value 并移动到头部

            node = self.cache[key]

            node.value = value

            self._move_to_head(node)

        else:

            # 如果是新 key

            new_node = self.DLinkedNode(key, value)

            self.cache[key] = new_node

            self._add_to_head(new_node)

            self.size += 1

            # 检查是否超出容量

            if self.size > self.capacity:

                # 淘汰最久未使用的节点（尾部节点）

                removed_node = self._remove_tail()

                # 从哈希表中删除

                del self.cache[removed_node.key]

                self.size -= 1
```
