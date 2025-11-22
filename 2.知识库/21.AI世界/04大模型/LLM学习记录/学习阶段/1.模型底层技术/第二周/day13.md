<font color="#e36c09">整体维度的变换有点乱</font>：
# 缕清整体结构

1.  输入词（此时 shape 假设形状为（2，3），如 `[[1，2，3]，[4,5,6]] `，代表两个训练批次，每个训练批次有 3 个词语，(batch_size, seq_len)）
     - input embedding 处理（形状变为 (batch_size, seq_len, d_model)）
     - positional encoding 处理（形状不变，是在原理词向量的基础上加入位置）

2.  MultiHeadAttention:    此时词（batch，seq，d-model），接着词进入多头注意力机制。生成自己的 Q、K、V 向量。初始的时候是随机化的，但 shape 和自身一模一样。
     - .在函数里，将 QKV 拆分维度，变成（batch，seq，h，-1）也就是说把 d_model 变成 h * head_dim。拆分后，还需要换一下位置，把 h 和 seq 换一下方便接下来的点积运算
     - QK 形成 attentionk 矩阵，与 V 乘，最终维度是 (batch, h, seq, h_dim)。使用 transport、contiguous 和 view，把维度重新变成（btach，seq，d_model）
3.  Add&Norm：加入残差后层归一化，不改变维度
4. FeedForward：第一层线性，维度变为（btach，seq，dff），扩展了。第二层线性层，加个 relu，维度不变。第三层线性，linear (dff, d_model)，故不维度又变回（batch，seq，d_model）了。拓展再压缩，增加模型表达能力。<font color="#e36c09">往往看到很多神经网络都有这种操作，为什么要这样</font>：映射到高维度时，模型又能捕捉到好多复杂特征了，再加个 ReLu 引入非线性，总之本质是更全面捕捉信息，最后折叠就是还原嘛，想象成向量从地球进入一个更牛逼的空间捕获了更厉害的东西，然后回来地球继续做人，进行下一步，不过此时已经是“超人”了
5. 继续 Add&Norm
6. 进行 N 次以上这些操作，然后再进入 Linear，softmax，变成一堆概率。维度仍然是（batch，seq，d_model）


## Transformer 的 QA

## 自注意力每层的计算复杂度
  $QK^T$, 显然乘完后是 n×n 的矩阵（n 为 seq_len），即计算 $n^2$ 次，每次要有 d 次乘法，故共为 $O (n^2d)$ ，softmax 是 n 方。注意力矩阵与 V 矩阵页为 n 方 d，故最终计算复杂度为
$$O (n^2d)$$

## Adam
动量+自适应学习率+偏差校正


