# 层次
In the first stage (grpo jsonl.py) serving as a prepara-
tion stage, users can flexibly define custom reward functions
and prepare training data tailored to their tasks. The frame-
work also supports various VLMs through a modular VLM
Module Definition, which will be described in § 3.2. The
second stage (grpo trainer.py) manages the GRPO training
process. It begins with model initialization, followed by
confirmation of training parameters decided by the user-
custom parameters. We support LoRA fine-tuning, vision
tower freezing training, and full parameters training, which
could be adapted to distinct compute resources and task re-
quirements. The model subsequently generates multiple se-
quences, which are scored using the defined reward func-
tion. These reward signals are then used to compute the
GRPO loss for parameter optimization
VLM-R1 provides full support for GRPO training while
offering flexibility in reward design, model selection, and
optimization strategies, making it a versatile tool for RL-
based vision-language research.
一个部件是训练参数，一个部件是和VLM核心模块衔接的板块

# 奖励函数
它的“多模态”特性体现在**奖励函数的设计**上。

> **原文**: $Rrec_acc(q, o) = IoU(b*, frec(o))$

我们来拆解这个奖励函数，看看它是如何把“视觉”和“语言”连接起来的：

1. **o (VLM output sentence)**: 这是模型的**语言输出**，比如 <think>...</think><answer>{...[120, 250, 380, 490]...}</answer>。
    
2. **frec(o)**: 这是一个**解析函数**。它的作用是从这段语言输出中，**提取**出 [120, 250, 380, 490] 这个边界框坐标。
    
3. **b* (ground truth bounding box)**: 这是数据集中标注的**“标准答案”**边界框。
    
4. **$IoU(b*, frec(o))$**: **这才是“魔法”发生的地方！** IoU (Intersection over Union，交并比)是一个**纯粹的视觉评估指标**。它通过计算两个边界框的重合程度，来判断模型生成的框和标准答案的框有多接近。
    
    - 这个计算是在**图像空间**中完成的。
        

**所以，奖励函数 R 成为了连接语言世界和视觉世界的桥梁！**

- 模型在**语言世界**里生成一个答案 o。
    
- 奖励函数通过frec把答案里的坐标“翻译”回**视觉世界**，然后用IoU这个视觉世界的“尺子”去度量它，得到一个分数。
    
- 这个分数再被反馈给GRPO算法，用来优化那个在语言世界里做决策的模型。