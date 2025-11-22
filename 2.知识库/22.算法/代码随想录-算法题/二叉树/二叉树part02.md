最近一段时间刷算法时间花的有点少，
只整理了递归方法，且没有自己手过一遍，只是看
这段时间过了需重习二叉树
# 递归三部曲
1. 明确确定递归函数的参数和返回值
2. 确定终止条件
3. 确定单层递归逻辑
在确定递归逻辑时，是将大问题分解成更小的同类问题。抱着这个心态去写逻辑。同时，确保问题向”终止条件“坍缩


# 226翻转二叉树

```python
  def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:

        if root is None:

            return None

        root.left, root.right = root.right, root.left  # 交换左右儿子

        self.invertTree(root.left)  # 翻转左子树

        self.invertTree(root.right)  # 翻转右子树

        return root

```
# 101对称二叉树
全空，可以称之为”对称“
一空一非空，不可以称为”对称“

```python
if p is None or q is None:

                return p is q

```

在此基础上，确定left.right 与 right.left的节点相等，以达到对称的效果
```python
def isSameTree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:

            if p is None or q is None:

                return p is q

            return p.val == q.val and isSameTree(p.left, q.right) and isSameTree(p.right, q.left)
            
def isSymmetric(self, root: Optional[TreeNode]) -> bool: 

        return isSameTree(root.left, root.right)

```
# 104 二叉树最大深度
层次遍历的基础上，每一层记depth+=1
```python
def maxDepth(self, root: Optional[TreeNode]) -> int:

        if not root:

            return 0

        depth = 0

        queue = collections.deque([root])

        while queue:

            depth += 1

            for _ in range(len(queue)):

                node = queue.popleft()

                if node.left:

                    queue.append(node.left)

                if node.right:

                    queue.append(node.right)

        return depth

```
