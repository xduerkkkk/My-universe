

# 共享权重有哪些
首先decoder和encoder在处理同语言的时候 共享embedding 很好理解

然后就是，decoder的embedding和最后lmhead的全连接层也共享。
这是为啥呢
embedding是把词变成向量  叫词嵌入
lmhead 是看我们训练出的向量  最有可能是什么词 hidden_size, vocab_size

# 计算瓶颈
一个核心的数学知识：  
**一个 `[m, n] 矩阵乘以一个 [n, p] `矩阵，其FLOPs大约是 2 * m * n * p。**
很容易理解，我们最终得到的是m，p矩阵，共用m * P 次操作，
那么每次大操作又含多少小操作呢  是n维度的对齐， 总共n次乘法n次加法，所以还要×2N

下面一个环节一个环节看
假设我们只传入1个token 也就是我们操作的维度是`[1,hidden_state]` 后面简化为`[1,d]`

## FFN
up_proj  升维度，一般升到4d去， 显然， 是一个8d方
down_proj 回来，1，4d    ×    4d，d    根据核心公式我们知道，是8d方
总前向16d，反向传播是前向传播2倍 所以总共是48d方

## QKVO投影
首先生成qkv向量， 是把1,d 乘 d，d      是2d方  
还有out_proj 也是把1，d 乘 d，d        也是2d方
所以很简单， 是3乘8d方  24d方

## attention计算核心
我们仍然是看单token的计算量，即推理状况
也就是我们已经处理了L个token，现在要处理第L+1个token。
我们生成的q向量是1，d
整个KV矩阵， 他们的形状全都是`[seq_len,hidden_state]` 我们简化为L+1，d
首先Q向量与K矩阵相乘， 1，d 乘 d，L+1           2d（L+1）
现在新的注意力权重是1，L+1
V矩阵是L+1,d       所以2d（L+1）
前向传播4d（L+1）




- FFN和QKVO投影的计算量**只和d有关**。
    
- 核心Attention计算的计算量**和L有关**

### **1. 为什么反向传播的计算量约等于前向传播的2倍？**

这是一个很好的、基于计算图的“经验法则”。我们用一个简单的线性层y = x @ W来理解。

- **前向传播 (Forward Pass)**:
    
    - **计算**: y = x @ W
        
    - **FLOPs**: 2 * m * n * p (假设x是[m,n], W是[n,p])
        
    - **目的**: 计算输出y。
        
- **反向传播 (Backward Pass)**:
    
    - **输入**: 上游传来的梯度 dL/dy (损失L对输出y的梯度)。
        
    - **目的**: 需要计算**两个**梯度：
        
        1. **权重的梯度 dL/dW**: 用来更新权重。根据链式法则，dL/dW = x.T @ (dL/dy)。这是一个 [n,m] @ [m,p] 的矩阵乘法，FLOPs约为 2 * n * m * p。
            
        2. **输入的梯度 dL/dx**: 需要继续往下一层传播。根据链式法则，dL/dx = (dL/dy) @ W.T。这是一个 [m,p] @ [p,n] 的矩阵乘法，FLOPs约为 2 * m * p * n。
            
    - **总FLOPs**: 2*n*m*p + 2*m*p*n = 4*m*n*p。
        
- **对比**:
    
    - FLOPs_backward = 4 * m * n * p
        
    - FLOPs_forward = 2 * m * n * p
        
    - 所以，FLOPs_backward = 2 * FLOPs_forward。
        

**结论**: 对于一个标准的线性层，反向传播需要计算对权重和对输入的梯度，这两次矩阵乘法的计算量加起来，正好是前向传播那一次矩阵乘法计算量的**两倍**。这个1:2的比例，是估算整个网络训练FLOPs的一个非常常用的近似。


- **训练 (Training)**:
    
    - 时间复杂度: O(s² * d)
        
    - 显存瓶颈: O(s²) (来自激活值)
        
- **推理 (Inference)**:
    
    - **第一步：预填充 (Prefill)**，处理长度为s_prompt的初始提示词。
        
        - 时间复杂度: O(s_prompt² * d)
            
        - 这一步没有激活值缓存，但需要生成并存储KV_cache，显存占用O(s_prompt * d)。
            
    - **第二步：解码 (Decoding)**，逐词生成。
        
        - 生成第k个新词时（此时总长度为s_prompt + k），**这一步**的时间复杂度是 O((s_prompt + k) * d)。
            
        - **总解码时间**是 Σ O((s_prompt + k) * d)，累加起来，总体上还是一个**平方级别**的复杂度。

# 在架构上解决计算复杂

## Sparse attention
- 滑动窗口注意力 每个token只做与他邻接的，一个窗口内的，tokens的注意力。 从n方，降低到n×w ？？  咦，之前推理了，单个token，注意力分数是n乘n的矩阵，所以n方的复杂度，现在为啥，是n乘w呢？
- 膨胀窗口注意力： 跳着看 扩大感受野
- 全局＋随机


**A. 标准自注意力 (Full Attention)**

- **计算什么？**: 我们需要计算一个巨大的[n, n]的注意力得分矩阵。
    
- **如何计算？**:
    
    - 为了计算这个矩阵的**第一行**（即第一个token对所有token的注意力），我们需要做1个Query向量和n个Key向量的点积。计算量是O(n * d)。
        
    - 为了计算**整个**[n, n]矩阵，我们需要对**每一个**Query（总共n个）都重复这个过程。
        
    - **总计算量**: n * O(n * d) = O(n² * d)。
        
- **结论**: 复杂度是O(n²*d)，瓶颈在n²。
    

**B. 滑动窗口注意力 (Sliding Window Attention)**

- **计算什么？**: 我们**不再**计算那个完整的[n, n]矩阵。对于每个token，我们只计算它和它窗口w内的邻居的注意力得分。
    
- **如何计算？**:
    
    - **对于第一个token**: 它只关注自己和右边w/2个邻居，总共大约w个token。计算它的注意力得分行，只需要做1个Query向量和w个Key向量的点积。计算量是O(w * d)。
        
    - **对于第二个token**: 它也只关注自己左右w/2范围内的w个邻居。计算它的注意力得分行，计算量也是O(w * d)。
        
    - ...
        
    - **对于第n个token**: 它的计算量还是O(w * d)。
        
- **总计算量**:
    
    - 我们总共有n个token。
        
    - **每一个**token的注意力计算量都是O(w * d)。
        
    - **总计算量**: n * O(w * d) = O(n * w * d)。
        
- **结论**: 复杂度是O(n*w*d)。因为w是一个固定的、远小于n的超参数，所以我们说复杂度从**二次**O(n²)降低到了**线性**O(n)


## GQA/MQA
MHA：标准的多头注意力，qkv均被切分，配对。 这样的话，kvcache和标准注意力的kvcache没区别
MQA：我不叫multiHead了，我叫MultiQuery，我只是多查询头，k和v不切分，所有头共享一个k一个v。但我没理解为什么降低kvcache了， k和v切分不切分，总和维度不都是hiddenstate吗
GQA：依然多query头，我们把query头分组，比如分g个组，然后每个组配套一个k，一个v
也就是有g个k和v  query仍然多

**正确的逻辑是**:

1. **Query头的数量和维度是基准，是固定不变的** (num_Q_heads * head_dim = hidden_size)。
    
2. MQA和GQA**只减少了Key和Value头的数量**，但**没有改变任何头的head_dim**。head_dim必须保持一致，否则Query和Key之间将无法进行点积运算。
    
3. 因此，在Cache_Size的计算公式 bs * seq_len * (num_K_heads + num_V_heads) * head_dim 中，**head_dim是一个常数**（比如128），而变量是num_K_heads和num_V_heads。
    

**所以，这个对比是完全成立的**:

- MHA: 32 * 128
    
- MQA: 2 * 128
    
- GQA: 8 * 128
    

MQA的KV缓存大小，就是MHA的 (2*128) / (32*128) = 2/32 = 1/16。

**一个最后的细节：参数量**

- **Q的投影矩阵W_q**: 在所有模式下，大小都是 [hidden_size, hidden_size]，即 [2048, 2048]。
    
- **K的投影矩阵W_k**:
    
    - MHA: 大小是 [hidden_size, hidden_size] -> [2048, 2048]
        
    - MQA: 因为只需要生成一个128维的K头，所以大小是 [hidden_size, head_dim] -> [2048, 128]
        
    - GQA: 因为需要生成4个128维的K头，所以大小是 [hidden_size, num_K_heads * head_dim] -> [2048, 4 * 128] = [2048, 512]
        
- W_v同理。所以GQA/MQA不仅减少了KV缓存，也减少了模型的**参数量**。

