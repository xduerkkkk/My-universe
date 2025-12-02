我们回顾一下transformer的强大，
最原始的，2017年的论文中，是encoder和decoder的组合  
送入一个句子 encoder能输出对此句子的理解  （输出一样的形状，但包含的每一个词向量都蕴含上下文语境）
decoder能依照理解 输出“翻译” 
我们还衍生出encoder-only 专门做理解的模型，如Bert
衍生出decoder-only 专门用于生成文字的模型，如GPT、Gemini、DeepSeek。
其中，decoder-only可以理解为最火、最适众的ai模型，我们称大语言模型一般情况都是指题目。


不知道大家是否记得，对于AI发展，似乎无数业界大佬都有不同看法，
李飞飞说要往”世界模型、具身智能“转变，**Yann LeCun** 认为我们未来一定会找到”新范式“，
还有稍微”悲观“点的， Transformer之父 Jones说”他受够了transformer，是时候突破了，现在就像Transformer 出现前的那段时期，研究人员们无休止地调整循环神经网络（RNN）以获取微小的增量收益“

我们不禁疑惑，
是什么，让Transformer没有在当今”继续发力“，没有继续像23年发布chatgpt一样引爆AI界。他的缺陷是什么，被榨干了吗？
我曾经写过正宗transformer架构，  
而这几年来，各大模型，llama，gpt，deepseek，他们用的，虽然也是transformer架构，虽然也是decoder-only，但是否和传统的有很大区别？


接下来的文章，我们一起去探索transformer的缺陷，以及目前业界的改进。
仍然，我会保持文章风格，通俗易懂，不陷入任何高深的数学计算（这些会另开文章）
我会给大家，建立起，”Sparse attention, flashattention,kv cache,MQA/GQA/MLA,RoPE “，这些大模型圈子里高频名词的直觉理解。