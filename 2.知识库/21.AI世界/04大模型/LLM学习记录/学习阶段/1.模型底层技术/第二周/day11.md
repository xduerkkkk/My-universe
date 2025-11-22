# 手撕 transformer
## 背景
实际上 attention 在 transformer 之前就有了，只不过大家都是结合着 rnn 使用。rnn：
$$h_t = f(W_hh_{t-1}+W_xx_t+b) $$
 $h_t$ 是时间步 $t$ 的隐藏状态， $f$ 是激活函数（如tanh或ReLU）= $W_h$ 是隐藏状态的权重矩阵 \item $h_{t-1}$ 是前一个时间步的隐藏状态 , $W_x$ 是输入 $x_t$ 的权重矩阵, $b$ 是偏置项.
 可见 rnn 依赖短时序列，同时无法并行处理数据
 transformer 告诉大家，不用 rnn，attention 机制就够了！就好像后面的 gpt，告诉大家，数据够大模型就好了，数据就够了！deepseek 告诉大家，在预训练与 SFT 过程不用那么繁琐，一个精致又简单的 RLHF就够了！大道至简，做减法反而是一种优化。Transformer 就是一种减法。
 当然，Transformer 还加入了 selfattention 和位置编码的概念。不过这不影响它的减法之美

## scaled_dot
qk (batch, head_n, seq/sek, dim) 矩阵相乘，（k 矩阵最后两个维度要转换顺序），经过 softmax 后，继续与 v 矩阵(batch, head_n, seqk, dim)相乘，此时维度显然为 (batch, head_n, seqv, dim)