# 二叉树迭代遍历
递归法比较简单，这里直接上用栈模拟
前序与后序类似，中序需要单独区分

```python
def preorderTraversal(root):
    if not root:
        return []
    
    stack = [root]
    result = []

    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:  # 先压入右孩子（因为栈是后进先出）
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result

```

```python
# 中序遍历-迭代-LC94_二叉树的中序遍历

    def inorderTraversal(self, root: TreeNode) -> List[int]:

        if not root:
            return []
        stack = []  # 不能提前将root节点加入stack中

        result = []
        cur = root
        while cur or stack:
            # 先迭代访问最底层的左子树节点
            if cur:     
                stack.append(cur)
                cur = cur.left		
            # 到达最左节点后处理栈顶节点    
            else:		
                cur = stack.pop()
                result.append(cur.val)
                # 取栈顶元素右节点
                cur = cur.right	
        return result
```

```python

 def postorderTraversal(self, root: TreeNode) -> List[int]:
        if not root:
            return []
        stack = [root]
        result = []
        while stack:
            node = stack.pop()
            # 中节点先处理
            result.append(node.val)
            # 左孩子先入栈
            if node.left:
                stack.append(node.left)
            # 右孩子后入栈
            if node.right:
                stack.append(node.right)
        # 将最终的数组翻转
        return result[::-1]
```

```

```

# 二叉树层序遍历

```python
def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:

        if root is None:

            return []

        ans = []

        q = deque([root])

        while q:

            vals = []

            for _ in range(len(q)):

                node = q.popleft()

                vals.append(node.val)

                if node.left:

                    q.append(node.left)

                if node.right:

                    q.append(node.right)

            ans.append(vals)

        return ans

```
注意，ans除外（不参与算法，只记录答案），有两个列表
q.append，q pop出3，让vals是3， 3拓展的9和20放入q里面，
记录vals，下一个循环“while q”开始循环q中的9和20
不要把vals和q混淆
## 补充

```python
class Solution:

    def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:

        if not root:

            return []

        q = collections.deque([root])

        ans = []

        while q :

            vals = []

            sum_ = 0

  

            for _ in range(len(q)):

                node = q.popleft()

                sum_ += node.val

                if node.left :

                    q.append(node.left)

                if node.right:

                    q.append(node.right)

            ans.append(sum_ / len(q))

        return ans

```

size = len(q)
ans.append(sum_ / size)
# 二叉树右视图
## 常规：
层次遍历，每一层的最后一个
```python
def rightSideView(self, root: TreeNode) -> List[int]:
        if not root:
            return []
        
        queue = collections.deque([root])
        right_view = []
        
        while queue:
            level_size = len(queue)
            
            for i in range(level_size):
                node = queue.popleft()
                
                if i == level_size - 1:
                    right_view.append(node.val)
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        
        return right_view
```
## 技巧
有点数学规律的意味了哈
```python
def rightSideView(self, root: Optional[TreeNode]) -> List[int]:

        ans = []

        def dfs(node,depth):

            if node is None:

                return

            if depth == len(ans):

                ans.append(node.val)

            dfs(node.right,depth + 1)

            dfs(node.left, depth + 1)

        dfs(root,0)

        return ans

```
