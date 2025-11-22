首先，传统的qkv计算中，有一个中间结果矩阵nn 在显存放着，我们要反复进行io读写，这些读写会耗费时间，而且nn矩阵很大还占内存。 但是，我们最终结果只是nd_k这个矩阵 ， 所以可以改变中间结果这样的方式呀。  
第一点，nn的矩阵是由softmax最终得来的，得益与数学，我们可以做到拆分，原来一个长度为n的行才能计算softmax，我们可以只把行分成块， 最后拼接起来仍然是长度为n的行的softmax结果  
第二点 然后我们将softmax这一行与v乘放到ndk矩阵里 于是我们最终，只有当前最大数，和当前sum，还有nd_k这些中间结果需要存储  
那么显存，读写速度，都加快了

# 代码实现
以lightllm项目，llama的models实现为例子。
首先，对于prefill阶段和decoding阶段，flashattention的实现是不同的
## prefill
**context_flashattention_nopad.py**
执行经典的flashattention，进行Tilinf、Online Softmax，

```python
# === 1. Online Softmax 初始化 ===
m_i = tl.zeros([BLOCK_M], dtype=tl.float32) - float("inf")
l_i = tl.zeros([BLOCK_M], dtype=tl.float32)
acc = tl.zeros([BLOCK_M, BLOCK_DMODEL], dtype=tl.float32)

# === 2. 分块遍历 K/V ===
for start_n in range(0, block_end_loc, BLOCK_N):
    # 获取物理位置
    kv_loc = tl.load(Req_to_tokens + ...)

    # 加载 K
    off_k = kv_loc[None, :] * stride_kbs + ...
    k = tl.load(K + off_k, ...)

    # QK 计算 + 缩放 + 掩码
    qk = tl.dot(q, k) * sm_scale
    mask = (offs_m + prompt_cache_len)[:, None] >= (start_n + offs_n)[None, :]
    qk = tl.where(mask, qk, -1.0e8)

    # 在线 softmax 核心
    m_ij = tl.maximum(m_i, tl.max(qk, 1))
    qk -= m_ij[:, None]
    p = tl.math.exp2(qk)
    l_ij = tl.sum(p, 1)

    alpha = tl.math.exp2(m_i - m_ij)
    l_i = l_i * alpha + l_ij
    acc = acc * alpha[:, None]

    # 加载 V 并累加
    v = tl.load(V + off_v, ...)
    acc = tl.dot(p.to(v.dtype), v, acc)
    m_i = m_ij

# === 3. 归一化输出 ===
acc = acc / l_i[:, None]
tl.store(Out + off_o, acc, ...)
```

**flashattention_infer_struct.py**
保存router传来的信息，记录cu_seqlens page_table
连接调度层和计算层

## Decoding
1. **Flash Decoding 系列在做什么？(关键！)**
    
    - 这正是我们上一轮讨论的，那个**“先并行，后汇总”**的极致优化！
        
    - **flash_decoding.py (总协调):** 它是总导演。当需要生成一个新词时，它启动这个两阶段计划。
        
    - **flash_decoding_stage1.py (并行计算):**
        
        - 总导演一声令下，这个脚本负责把KV Cache切成很多块，并让**多个GPU计算单元同时开始并行工作**。
            
        - 每个单元都独立计算自己那一小块的局部注意力结果，并保存一个**局部的**log-sum-exp统计值。
            
    - **flash_decoding_stage2.py (结果合并/Reduction):**
        
        - 当所有并行单元都完成工作后，这个脚本负责**“汇总”**。
            
        - 它收集所有局部的log-sum-exp，计算出**全局**的正确归一化参数。
            
        - 然后，用这个全局参数去修正每个并行单元的输出结果，并将它们相加，得到最终的、这一个token的输出。
            

2. **【Decoding循环开始】**
    
    - 循环生成第1个新token: 调用 flash_decoding.py。
        
        - flash_decoding.py 调用 stage1 并行计算所有KV Cache块。
            
        - flash_decoding.py 调用 stage2 汇总结果，得到第1个新token。
            
    - 循环生成第2个新token: 再次调用 flash_decoding.py...
        
    - ...直到生成结束符。

