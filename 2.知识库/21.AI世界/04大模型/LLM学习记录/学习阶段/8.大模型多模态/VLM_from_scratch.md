
# 核心模块VLM
## init





## forward
1. 文本处理 由llm的tokenizer处理。 输出
2. 图片占位符数量+文本token数量，512  
3. 图片processor， 将图片预处理，变为1，3，224，224  
4. 图片处理 我们的patch精度要求1616 那么就一共有1414个patch，共196。 所以，输出的是1，196，768. 768只是说hiddensize 是设置的精度  
5. 融合 先将3的维度，投影为 1，196，512， 刚才的文本处理是1，1，图片占位符数量+文本token数量，512 图片占位符数量刚好就是196， 所以可以直接加起来  
6. 推理 此时的combined_embedding 就为 1，196+文本token数量，512 可以直接送给llm推理 变成`[1, 196 + 文本长度, vocab_size]` 然后采样，输出token
## vlm 的 pretrain和sft

 首先我们本次项目的预训练数据，就是单轮图文对话  
那么我们的visonencoder，是使用现成的vit， 是clip模型中的vit单独摘录出来，这个会让图片向量靠近图片含义的文字向量。 
然后我们的语言模型也是训练好的。 那我们这个投影层， LLAva架构只是个linear嘛， 就是学把图片彻底翻译成文字 ，就是说vit出来是靠近文字向量， 它的向量维度实际都跟文本向量不一致， 而这里的linear直接是投影，把图片向量完全转化成文字向量的形状 那我们预训练时，只训练这个投影层， 就是为了让它翻译准确一点，

然后第二轮sft，我们训练的是llm注意力机制的qkv矩阵，我们是为了让模型能理解图片，所以用的多轮指令对话，是这样吗？  

所以两轮中，投影层只在第一次训练 llm 只在第二次训练 vit全程冻结 

1. **Stage 1 (Pre-train / Alignment)**:
    
    - **冻结**: ViT, LLM
        
    - **训练**: vision_proj
        
2. **Stage 2 (SFT / Instruction Tuning)**:
    
    - **冻结**: ViT
        
    - **训练**: vision_proj + language_model (或其LoRA部分)
## 对比架构

如qwenvl和gemini
他们的训练。就包含”眼睛“了， 预训练第一阶段只训练vit， 第二阶段vit和llm一起训练。
sft/dpo 指令微调和对齐，使用复杂任务
咦？那他们的那个vit到llm的投影呢？
Qwen-VL使用的是 **Patch Merging**
 ViT Features (1024, 1024) -> Reshape -> Merged Features (256, 4096) -> MLP -> LLM Features (256, 4096)
  1. **合并**: 通过reshape和permute操作，将空间上相邻的2x2=4个patch的特征向量，在**特征维度**上拼接起来。
  2. **投影**: 再用一个MLP对这个拼接后的、更长的向量进行处理和投影。
MiniCPM呢，使用的是 Resampler



```
ViT Features (N, D_vit) ---
                           |--- CrossAttention --> LLM Features (M, D_llm)
Learnable Queries (M, D_llm) --
```
1. **定义“问题”**: 模型在内部定义了一小组（比如M=64个）**可学习的**“查询向量 (Learnable Queries)”。你可以把它们想象成64个“记者”。
    
2. **“记者”提问**: 这64个“记者”（作为Query），去和ViT输出的海量patch特征（N个，作为Key和Value）进行一次**交叉注意力 (Cross-Attention)**。
    
3. **生成“摘要”**: 每个“记者”都会根据它和所有patch特征的交互，最终“写”出一份自己的“报道”，也就是一个输出向量。
    
4. 最终，无论ViT输出了多少个patch特征（N可以是196，也可以是1024），输出的永远是**固定数量（M=64个）**的、高度浓缩的“新闻摘要”向量