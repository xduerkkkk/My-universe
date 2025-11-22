`collections` 是 Python 标准库中的一个非常有用的模块，它提供了许多用于数据处理的高效容器类型。除了 `Counter` 之外，`collections` 模块中还有许多其他常用的类和函数，这些也经常被导入和使用。以下是一些常见的内容：

### 1. `defaultdict`
`defaultdict` 是一个字典子类，它提供了一个工厂函数，用于自动初始化字典的默认值。

#### 示例
```python
from collections import defaultdict

# 创建一个默认值为 int（默认为0）的字典
d = defaultdict(int)
d['a'] += 1
print(d)  # 输出: defaultdict(<class 'int'>, {'a': 1})

# 创建一个默认值为 list 的字典
d = defaultdict(list)
d['a'].append(1)
print(d)  # 输出: defaultdict(<class 'list'>, {'a': [1]})
```

### 2. `deque`
`deque`（双端队列）是一个线程安全的双向队列，支持从两端高效地添加和删除元素。

#### 示例
```python
from collections import deque

# 创建一个 deque
dq = deque([1, 2, 3])
dq.append(4)  # 从右侧添加元素
dq.appendleft(0)  # 从左侧添加元素
print(dq)  # 输出: deque([0, 1, 2, 3, 4])

# 从右侧移除元素
dq.pop()
print(dq)  # 输出: deque([0, 1, 2, 3])

# 从左侧移除元素
dq.popleft()
print(dq)  # 输出: deque([1, 2, 3])
```

### 3. `OrderedDict`
`OrderedDict` 是一个字典子类，它记录了字典元素添加的顺序。从 Python 3.7 开始，普通字典也保证了插入顺序，但 `OrderedDict` 仍然在某些场景下有用，例如需要实现自定义的等价方法。

#### 示例
```python
from collections import OrderedDict

# 创建一个 OrderedDict
od = OrderedDict()
od['a'] = 1
od['b'] = 2
od['c'] = 3
print(od)  # 输出: OrderedDict([('a', 1), ('b', 2), ('c', 3)])

# 移动元素到末尾
od.move_to_end('a')
print(od)  # 输出: OrderedDict([('b', 2), ('c', 3), ('a', 1)])
```

### 4. `namedtuple`
`namedtuple` 是一个工厂函数，用于创建具有命名字段的元组子类。它使得元组的字段可以通过名称访问，而不仅仅是通过索引。

#### 示例
```python
from collections import namedtuple

# 创建一个 namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x)  # 输出: 1
print(p.y)  # 输出: 2

# namedtuple 也可以用于创建简单的数据结构
Person = namedtuple('Person', ['name', 'age'])
person = Person('Alice', 30)
print(person.name)  # 输出: Alice
print(person.age)  # 输出: 30
```

### 5. `ChainMap`
`ChainMap` 是一个用于将多个字典逻辑上组合成一个字典的类。它在查找时会按顺序在多个字典中查找键。

#### 示例
```python
from collections import ChainMap

# 创建两个字典
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

# 创建一个 ChainMap
chain_map = ChainMap(dict1, dict2)
print(chain_map['a'])  # 输出: 1
print(chain_map['b'])  # 输出: 2，因为 dict1 中的 'b' 优先于 dict2 中的 'b'
print(chain_map['c'])  # 输出: 4
```

### 6. `UserDict`, `UserList`, `UserString`
这些类是 `collections.abc` 模块中定义的抽象基类的具体实现，用于创建自定义的字典、列表和字符串类。

#### 示例
```python
from collections import UserDict

# 创建一个自定义字典
class MyDict(UserDict):
    def __getitem__(self, key):
        if key not in self.data:
            return f"{key} not found"
        return self.data[key]

my_dict = MyDict({'a': 1, 'b': 2})
print(my_dict['a'])  # 输出: 1
print(my_dict['c'])  # 输出: c not found
```

### 总结
`collections` 模块提供了许多强大的工具，可以帮助你更高效地处理数据。以下是一些常用的类和函数：
- `Counter`：用于计数的字典。
- `defaultdict`：提供默认值的字典。
- `deque`：双端队列。
- `OrderedDict`：有序字典。
- `namedtuple`：具有命名字段的元组。
- `ChainMap`：组合多个字典。
- `UserDict`, `UserList`, `UserString`：用于创建自定义的字典、列表和字符串。

这些工具在日常编程中非常有用，建议熟悉它们的用法。