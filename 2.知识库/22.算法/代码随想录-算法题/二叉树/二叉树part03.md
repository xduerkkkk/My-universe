# 判断是否为平衡二叉树

递归逻辑是
假如本次递归的主角叫B，B检查自己的左右平衡不，若不平衡则退出。若平衡，则将自己的最大深度交给自己的父节点A，让父亲A结合自己给的长度，和B的兄弟C的长度，判断是否平衡
![[二叉树part03-1748533453760.jpeg]]
```python

def isBalanced(self, root: Optional[TreeNode]) -> bool:
        return self.get_hight(root) != -1
    def get_hight(self, node):
        if not node:
            return 0
        left = self.get_hight(node.left)
        right = self.get_hight(node.right)
        if left == -1 or right == -1 or abs(left - right) > 1:
            return -1
        return max(left, right) + 1


```
# 二叉树的所有路径

![[二叉树part03-1748533985067.jpeg]]
“1，2，3”这一路应该很简单。
递归的性质，使得4之后的5，继续往左子树走，也就是不触发 'if not cur.left and not cur.right'不罢休
path.pop()使得能进行接着进行7、8

```python
class Solution:
    def traversal(self, cur, path, result):
        path.append(cur.val)  # 中
        if not cur.left and not cur.right:  # 到达叶子节点
            sPath = '->'.join(map(str, path))
            result.append(sPath)
            return
        if cur.left:  # 左
            self.traversal(cur.left, path, result)
            path.pop()  # 回溯
        if cur.right:  # 右
            self.traversal(cur.right, path, result)
            path.pop()  # 回溯

    def binaryTreePaths(self, root):
        result = []
        path = []
        if not root:
            return result
        self.traversal(root, path, result)
        return result
```
# 404 左叶子之和
分解为左子树和右子树的子问题
一个重要的逻辑是，只有**父节点**才能判断其左孩子是否是左叶子（叶子节点无法判断自身位置）
即
- 当前节点的左孩子存在（`root.left`），且左孩子是叶子节点（无左右子树）。
- ​**操作**：直接将左孩子的值赋给`leftValue`
```python
    def sumOfLeftLeaves(self, root):
        if root is None:
            return 0
        if root.left is None and root.right is None:
            return 0
        
        leftValue = self.sumOfLeftLeaves(root.left)  # 左
        if root.left and not root.left.left and not root.left.right:  # 左子树是左叶子的情况
            leftValue = root.left.val
            
        rightValue = self.sumOfLeftLeaves(root.right)  # 右

        sum_val = leftValue + rightValue  # 中
        return sum_val
```
# 222 完全二叉树节点个数
统计节点的递归法
```python
 def countNodes(self, root: TreeNode) -> int:
        return self.getNodesNum(root)
        
    def getNodesNum(self, cur):
        if not cur:
            return 0
        leftNum = self.getNodesNum(cur.left) #左
        rightNum = self.getNodesNum(cur.right) #右
        treeNum = leftNum + rightNum + 1 #中
        return treeNum
```