---

---
 
| python                                                                                                | C++                                                                                                                                                                 | 含义                                |     |
| ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- | --- |
| len(nums)                                                                                             | nums.size()                                                                                                                                                         | 数组长度                              |     |
| if nums[i] != 0                                                                                       | if nums[i]                                                                                                                                                          | ？                                 |     |
| nums[left],nums[right] = nums[right],nums[left]                                                       | swap(nums...)                                                                                                                                                       | 交换                                |     |
| left,right = 0, len(nums)-1                                                                           | int left = 0, right = nums.size() - 1;                                                                                                                              | 在C++中，同一行声明多个同类型变量时，类型名（int）只写一次。 |     |
| `ans =[0]* len(nums)`                                                                                 | `vector<int> ans(nums.size())`                                                                                                                                      |                                   |     |
| for c in s                                                                                            | for(char c : s)                                                                                                                                                     |                                   |     |
| Python 语法 (dict)                                                                                      | C++ 语法 (std::unordered_map)                                                                                                                                         | 解释                                |     |
| (内置)                                                                                                  | #include <unordered_map>                                                                                                                                            | 引入头文件                             |     |
| inorder_map = {}                                                                                      | std::unordered_map<int, int> inorder_map;                                                                                                                           | 创建一个int到int的哈希表                   |     |
| inorder_map = {val: i for i, val in enumerate(inorder)}                                               | for(int i=0; i<inorder.size(); ++i) { inorder_map[inorder[i]] = i; }                                                                                                | 遍历并填充哈希表                          |     |
| idx = inorder_map[val]                                                                                | int idx = inorder_map[val];                                                                                                                                         | 根据key获取value                      |     |
| <br>queue = deque()  使用append、popleft<br>                                                             | <br>`std::queue<int> queue`; 使用push、pop<br>                                                                                                                         |                                   |     |
| ```stack = []```                                                                                      | ```<br>std::stack<int> stack;<br>```使用push、pop                                                                                                                      |                                   |     |
| ```import heapq              priority_queue =[] heapq.heappush(priority_queue, (1, "task1"))  # 入队``` | ```cpp<br>#include <queue><br>#include <vector><br><br>std::priority_queue<int> priority_queue;<br>priority_queue.push(1);  // 入队<br>priority_queue.push(2);<br>``` |                                   |     |
| ```python<br>min_heap = []<br>heapq.heappush(min_heap, 1)<br>heapq.heappush(min_heap, 2)<br>```       | ```cpp<br>// 最小堆<br>std::priority_queue<int, std::vector<int>, std::greater<int>> min_heap;<br>min_heap.push(1);<br>```                                             |                                   |     |







# python的传参
### **“标签”的独立人生——图解`my_list = [9, 9, 9]`**

**1. 初始状态 (调用`modify(data)`后，进入函数的第一瞬间)**

*   内存的“堆”区，有一个`list`对象：`[1, 2, 3]`。
*   **全局**命名空间里，有一张标签 `data`，贴在这栋房子上。
*   `modify`函数的**局部**命名空间里，有一张**新的、独立的**标签 `my_list`，也贴在这**同一栋**房子上。

**图示:**
```
     全局空间            函数modify的局部空间
   +---------+         +-----------+
   |  data   | ---->   |  my_list  |
   +---------+         +-----------+
        |                     |
        |       +---------------------------+
        +-----> | list object: [1, 2, 3]    |
                +---------------------------+
```
**关键：** `data`和`my_list`是**两张**不同的纸，只不过它们上面，恰好写了**同一个**地址。

**2. 执行`my_list.append(100)`时，发生了什么？**

*   Python通过`my_list`这张标签，找到了`[1, 2, 3]`这栋房子。
*   它**直接在这栋房子上**施工，加了一个房间`100`。
*   房子本身被改造了。
*   因为`data`标签也贴在这栋房子上，所以通过`data`看，房子也变了。

**3. 【关键】执行`my_list = [9, 9, 9]`时，发生了什么？**

这个 `=` (赋值) 操作，对于“标签”来说，永远只做一个动作：**“撕下，然后重贴”**。

*   **第一步：** Python先在“堆”上，创建了**一栋全新的**`list`房子：`[9, 9, 9]`。
*   **第二步：** Python拿起了`my_list`这张**局部**标签，把它从`[1, 2, 3]`那栋旧房子上，**“撕”**了下来。
*   **第三步：** Python把`my_list`这张标签，**“贴”**到了`[9, 9, 9]`这栋新房子上。

**图示 (执行完`my_list = ...`之后):**
```
     全局空间            函数modify的局部空间
   +---------+         
   |  data   | ---->      (my_list标签已经不指向这里了)
   +---------+         
        |                
        |       +---------------------------+
        +-----> | list object: [1, 2, 3]    |
                +---------------------------+

                       +-----------+
                       |  my_list  |
                       +-----------+
                             |
                +---------------------------+
                | list object: [9, 9, 9]    | <--- my_list改贴到这里了
                +---------------------------+
```

**您看，从始至终，`data`这张全局标签，有人碰过它吗？**
**没有！** 它一直安安静静地，贴在`[1, 2, 3]`那栋老房子上。

**4. `modify`函数结束**
*   `modify`函数的“局部空间”被销毁。
*   `my_list`这张**局部**标签，连同它指向`[9, 9, 9]`的这个关系，一同“灰飞烟灭”。
*   （Python的垃圾回收机制，会发现`[9, 9, 9]`这栋房子，已经没有任何标签贴在它身上了，于是就会把它拆除回收）。

**5. `print(data)`**
*   Python通过`data`这张标签，找到的，依然是那栋从未被“重贴”过的、最初的`[1, 2, 3]`房子。

---

**终极结论**

*   **修改对象内部 (`my_list.append(...)`)：** 是**“原地施工”**。因为函数内外的标签，指向的是**同一个**被施工的对象，所以函数外的`data`能看到变化。
*   **重新赋值变量 (`my_list = ...`)：** 是**“标签改嫁”**。它只改变了函数**内部**那张**局部**标签的“婚姻关系”，让它指向了一个新的对象。它与函数**外部**的那张`data`标签，毫无关系。

这，就是Python“共享传参”模型最精妙、也最容易混淆的地方。
