# 513找树左下角的值
找到树最后一行的最左边的值

还记得层序遍历吧
```python
def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:

        if root is None:

            return []

        ans = []

        q = deque([root])

        while q:

            vals = []

            for i in range(len(q)):

                node = q.popleft()

                vals.append(node.val)

                if node.left:

                    q.append(node.left)

                if node.right:

                    q.append(node.right)

            ans.append(vals)

        return ans

```
显然，我们只要最后一层的第一个就是答案了
怎么修改逻辑呢？
我们不用ans了哈，我们只要一个数
即在循环中，第一个数
为result
```python
			if i == 0:
                    result = node.val
```
递归法与回溯法比较难，我还没时间消化，先记录下来
```python
class Solution:
    def findBottomLeftValue(self, root: TreeNode) -> int:
        self.max_depth = float('-inf')
        self.result = None
        self.traversal(root, 0)
        return self.result
    
    def traversal(self, node, depth):
        if not node.left and not node.right:
            if depth > self.max_depth:
                self.max_depth = depth
                self.result = node.val
            return
        
        if node.left:
            depth += 1
            self.traversal(node.left, depth)
            depth -= 1
        if node.right:
            depth += 1
            self.traversal(node.right, depth)
            depth -= 1
```
# 112 路径总和
给定一个二叉树和一个目标和，判断该树中是否存在根节点到叶子节点的路径，这条路径上所有节点值相加等于目标和。

一个**小巧思**：
计数器如何统计这一条路径的和呢？
不要去累加然后判断是否等于目标和，那么代码比较麻烦，可以用递减，让计数器count初始为目标和，然后每次减去遍历路径节点上的数值。
如果最后count == 0，同时到了叶子节点的话，说明找到了目标和。
如果遍历到了叶子节点，count不为0，就是没找到。
```python
class Solution:
    def traversal(self, cur: TreeNode, count: int) -> bool:
        if not cur.left and not cur.right and count == 0: # 遇到叶子节点，并且计数为0
            return True
        if not cur.left and not cur.right: # 遇到叶子节点直接返回
            return False
        
        if cur.left: # 左
            count -= cur.left.val
            if self.traversal(cur.left, count): # 递归，处理节点
                return True
            count += cur.left.val # 回溯，撤销处理结果
            
        if cur.right: # 右
            count -= cur.right.val
            if self.traversal(cur.right, count): # 递归，处理节点
                return True
            count += cur.right.val # 回溯，撤销处理结果
            
        return False
    
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if root is None:
            return False
        return self.traversal(root, targetSum - root.val) 
```
那如果题目给定一个二叉树和一个目标和，找到所有从根节点到叶子节点路径总和等于给定目标和的路径
如何在刚才不需要返回路径的代码上修改？
毫无疑问我们得用result数组记录结果，还要有path数组用于回溯
```python
  if not cur.left and not cur.right and count == 0: # 遇到叶子节点，并且计数为0
            return True
        if not cur.left and not cur.right: # 遇到叶子节点直接返回
            return False
        

```
修改为

```python

if not cur.left and not cur.right and count == 0: # 遇到了叶子节点且找到了和为sum的路径
            self.result.append(self.path[:])
            return

        if not cur.left and not cur.right: # 遇到叶子节点而没有找到合适的边，直接返回
            return
```

左子树和右子树部分 修改逻辑一样，展示一下左


```python
		if cur.left: # 左
            count -= cur.left.val
            if self.traversal(cur.left, count): # 递归，处理节点
                return True
            count += cur.left.val # 回溯，撤销处理结果

```
修改为

```python

if cur.left: # 左 （空节点不遍历）
            self.path.append(cur.left.val)
            count -= cur.left.val
            self.traversal(cur.left, count) # 递归
            count += cur.left.val # 回溯
            self.path.pop() # 回溯
```


# 从中序与后序遍历序列构造二叉树
难点，需自己手写
记录一下

```python

  def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode:
        # 第一步: 特殊情况讨论: 树为空. 或者说是递归终止条件
        if not preorder:
            return None

        # 第二步: 前序遍历的第一个就是当前的中间节点.
        root_val = preorder[0]
        root = TreeNode(root_val)

        # 第三步: 找切割点.
        separator_idx = inorder.index(root_val)

        # 第四步: 切割inorder数组. 得到inorder数组的左,右半边.
        inorder_left = inorder[:separator_idx]
        inorder_right = inorder[separator_idx + 1:]

        # 第五步: 切割preorder数组. 得到preorder数组的左,右半边.
        # ⭐️ 重点1: 中序数组大小一定跟前序数组大小是相同的.
        preorder_left = preorder[1:1 + len(inorder_left)]
        preorder_right = preorder[1 + len(inorder_left):]

        # 第六步: 递归
        root.left = self.buildTree(preorder_left, inorder_left)
        root.right = self.buildTree(preorder_right, inorder_right)
        # 第七步: 返回答案
        return root
```


