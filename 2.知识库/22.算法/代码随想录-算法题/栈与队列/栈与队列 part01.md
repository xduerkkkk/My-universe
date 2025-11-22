# 用栈模拟队列
列表的pop 与append都是对列表最后一个元素位置进行操作的，故而"先进后出（先进的在列表前面）" 属于栈
题目为用两个栈，即两个列表
模拟队列
后面的描述中栈就是列表，列表就是栈

那么对列的pop，是把最开始的元素pop出来
怎么操作？
将列表反转再pop不就好了吗？

每次调用pop的时候，不能每次都把列表反转嘛 乱套了
于是用两个栈  
调用pop时把in的列表反转到out列表里
push的时候push到in列表里
这两个列表，虽然不是直观的连续数据的队列
但完美满足所有的函数功能
```python
class MyQueue:

  

    def __init__(self):

        self.in_stack = []

        self.out_stack = []

  

    def push(self, x: int) -> None:

        self.in_stack.append(x)

  

    def pop(self) -> int:

        if self.out_stack:

            return self.out_stack.pop()

        else:

            for i in range(len(self.in_stack)):

                self.out_stack.append(self.in_stack.pop())

        return self.out_stack.pop()

  

    def peek(self) -> int:

        if self.out_stack:

            return self.out_stack[-1]

        else:

            for i in range(len(self.in_stack)):

                self.out_stack.append(self.in_stack.pop())

        return self.out_stack[-1]

  

    def empty(self) -> bool:

        if (self.out_stack or self.in_stack):

            return False

        else:

            return True

```
# 用队列模拟栈
队列只能popleft，也就是对第一个元素处理
那与上面栈模拟队列思路一样
反转再popleft不就好了？
```python
class MyStack:

    def __init__(self):

        self.stack = deque()
  

    def push(self, x: int) -> None:

        self.stack.append(x)
  

    def pop(self) -> int:

        if self.empty():

            return None

        for _ in range(len(self.stack)-1):

            self.stack.append(self.stack.popleft())

        return self.stack.popleft()



    def top(self) -> int:

        if self.empty():

            return None

        return self.stack[-1]

  

    def empty(self) -> bool:

        if self.stack:

            return False

        else:

            return True

```
# 20有效的括号

```python
def isValid(self, s: str) -> bool:

        stack = []

        for item in s:

            if item == '(':

                stack.append(')')

            elif item == '{':

                stack.append('}')

            elif item == '[':

                stack.append(']')

            elif not stack or stack[-1] != item:

                return False

            else:

                stack.pop()

```
# 1047 删除字符串中的所有相邻重复项

错误演示：
stack【-2】是可能越界的，而且看这两次stack.pop()，显然不优雅
```python
stack = []

        for i in range(len(s)):

            stack.append(i)

            while stack[-1] == stack [-2]:

                stack.pop()

                stack.pop()

        return ''.join(stack)

```
以下显然更优雅

```python
def removeDuplicates(self, s: str) -> str:

        stack = []

        for char in s:

            if stack and stack[-1] == char:#直接不把char放进stack里了

                stack.pop()

            else:

                stack.append(char)

  

        return ''.join(stack)

```
