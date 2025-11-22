
```c++
// MyVector.h
#pragma once // 防止头文件被重复包含

class MyVector {
private: // 这些是内部零件，不对外暴露
    int* m_data;      // 指向我们申请的连续内存的“基石”指针
    size_t m_size;    // 当前存储的元素个数
    size_t m_capacity; // 当前已申请的内存总容量

public: // 这些是提供给外部使用的“功能按钮”
    MyVector();                     // 构造函数 (盖房子的工人)
    ~MyVector();                    // 析构函数 (拆房子的工人)

    void push_back(int val);
    int get(int index);
    // ... 其他函数
};

```
