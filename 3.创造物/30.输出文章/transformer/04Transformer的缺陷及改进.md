我们回顾一下transformer的强大，

2017年，那篇论文横空出世，确立了**Encoder-Decoder**的标准架构。

- 送入一个句子，**Encoder** 负责输出“深度理解”（蕴含上下文语境的词向量）；
- **Decoder** 负责依照理解，输出“翻译”结果

随后，我们还衍生出俩种模型
- **Encoder-only** ，专门做极致理解的模型，如Bert
- **Decoder-only** ，专门用于生成文字的模型，如GPT、Gemini、DeepSeek。
其中，当我们提到“大语言模型（LLM）”时，指的几乎都是 **Decoder-Only** 架构。它也是最火、最融入我们生活的AI形态。

但是，不知道大家是否留意到，对于AI的未来，业界大佬们似乎都有着某种“焦虑”。

- 李飞飞说要往”世界模型、具身智能“转变，
- Yann LeCun认为当下LLM很不聪明，我们未来一定会找到”新范式“，
-  Transformer之父 Jones 也是语出惊人：”我受够了transformer，现在就像Transformer 出现前的那段时期，研究人员们无休止地调整循环神经网络（RNN）以获取微小的增量收益,是时候突破了"

我们不禁疑惑，
是什么，让Transformer没有在当今”继续发力“，没有继续像23年发布chatgpt一样引爆AI界。他的缺陷是什么，被榨干了吗？
我曾经写过正宗transformer架构，  
而这几年来，各大模型，llama，gpt，deepseek，他们用的，虽然也是transformer架构，虽然也是decoder-only，但是否和传统的有很大区别？


接下来的文章，我们一起去探索transformer的缺陷，以及目前业界的改进。
仍然，我会保持文章风格，通俗易懂，不陷入任何高深的数学计算（数学计算、严谨过程等会另开文章）
我会给大家，建立起”Sparse attention, MQA/GQA/MLA,RoPE..... “，这些大模型圈子里高频名词的直觉理解。


# Transformer的计算复杂度

我们已经清楚Transformer的架构了，下面可以讨论讨论，