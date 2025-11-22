message经过apply_chat_template 称为text
message也经过process_vision_info 得到image_input , video_input
- 具体是extract_vision_info 吧info字段提取出来
- 对这些vision_info 使用fetch_image或fetch_video 得到最终的input

此时，test

1. **特殊Token**: 认识它们，知道它们是“语法”，在微调时必须正确使用。
    
2. **Padding与Attention Mask**: 理解Padding是为了对齐长度，而attention_mask才是告诉模型忽略Padding的关键。永远确保你的数据处理流程正确生成了attention_mask。
    
3. **核心输入**: 知道processor最终会产出三大核心“食材”：
    
    - input_ids: 文本内容，包含特殊Token。
        
    - pixel_values: 图片/视频内容，已被处理成张量。
        
    - image_grid_sizes: 图片的空间布局信息，是多模态位置编码的基石。




## 所有接受的东西（图片、视频、文本）进入模型前
Mrope

```python
        # if we get 4D attention mask we cannot calculate rope deltas anymore. TODO @raushan fixme

        if position_ids is None and (attention_mask is None or attention_mask.ndim == 2):

            # calculate RoPE index once per generation in the pre-fill stage only

            if (

                (cache_position is not None and cache_position[0] == 0)

                or self.rope_deltas is None

                or (past_key_values is None or past_key_values.get_seq_length() == 0)

            ):

                position_ids, rope_deltas = self.get_rope_index(

                    input_ids,

                    image_grid_thw,

                    video_grid_thw,

                    second_per_grid_ts,

                    attention_mask,

                )

                self.rope_deltas = rope_deltas

            # then use the prev pre-calculated rope-deltas to get the correct position ids

            else:

                batch_size, seq_length, _ = inputs_embeds.shape

                delta = (

                    (cache_position[0] + self.rope_deltas).to(inputs_embeds.device)

                    if cache_position is not None

                    else 0

                )

                position_ids = torch.arange(seq_length, device=inputs_embeds.device)

                position_ids = position_ids.view(1, -1).expand(batch_size, -1)

                if cache_position is not None:  # otherwise `deltas` is an int `0`

                    delta = delta.repeat_interleave(batch_size // delta.shape[0], dim=0)

                position_ids = position_ids.add(delta)

                position_ids = position_ids.unsqueeze(0).expand(3, -1, -1)
```

## 图文交互
图文交互不是在一个“地方”发生的，而是通过三个协同工作的步骤实现的。你已经看过这三个步骤的代码，现在我们把它们串起来。

#### 魔法的第一步：“大一统”的输入序列 (inputs_embeds)

还记得在 Qwen2_5_VLForConditionalGeneration 的 forward 函数里那场“手术”吗？

codePython

````
inputs_embeds = inputs_embeds.masked_scatter(image_mask, image_embeds)```
这场手术的最终结果，就是我们得到的 `inputs_embeds`。

**这个 `inputs_embeds` 已经不再是纯文本的词向量序列了。它是一个“多模态混合序列”。**

想象一下这个序列：
`[vec("User"), vec(":"), vec_img_patch_1, vec_img_patch_2, ..., vec_img_patch_256, vec("Describe"), vec("this"), vec("image"), vec(".")]`

在这个序列里，代表文字的向量和代表图像patch的向量，**在地位上是完全平等的**。它们都是序列中的一个元素，肩并肩地站在一起。这是实现交互的**最根本前提**。

#### 魔法的第二步：“多模态身份证” (MRoPE)

虽然大家都是向量，但模型怎么知道哪个是文字，哪个是图片，图片patch在空间上又是怎么排列的呢？

这就是我们在进入LLM前计算的 `position_ids` 和 `self.rotary_emb` (也就是MRoPE)的作用！
```python
# in LLM forward function
position_embeddings = self.rotary_emb(hidden_states, position_ids)
````

position_embeddings 就是每个token的“多模态身份证”。

- 当token是文字时，身份证上写着“我是第 N 个文字”。
    
- 当token是图片patch时，身份证上写着“我是图片A，在第 H 行，第 W 列”。
    

这个“身份证”会被传递到每一层的self_attn模块中。

1. **第一步：打一个纯文本的“草稿”**
    
    codePython
    
    ```
    inputs_embeds = self.get_input_embeddings()(input_ids)
    ```
    
    - **输入**: input_ids，一个全是数字ID的序列，比如 [151644, 151645, 151857, ..., 151858, 198, 2610, ...]。其中 151857 可能就是特殊token <|image|> 的ID。
        
    - **输出**: inputs_embeds，一个词向量序列。现在，序列里的每一个位置都是一个向量了。但是，在 <|image|> 占位符位置上的那个向量，只是一个临时的、没有实际意义的“桩”，等待被替换。
        
2. **第二步：准备视觉“植入物”并进行“替换手术”**
    
    codePython
    
    ```
    # a. 从视觉模块获取处理好的图片特征
    image_embeds = self.get_image_features(pixel_values, image_grid_thw)
    
    # b. 找到手术位置（制作掩码）
    mask = input_ids == self.config.image_token_id
    # ... (扩展mask维度) ...
    image_mask = mask_expanded.to(inputs_embeds.device)
    
    # c. 执行手术
    inputs_embeds = inputs_embeds.masked_scatter(image_mask, image_embeds)
    ```
    
    - **动作**: masked_scatter 这个函数，就像一个精确的外科医生。它看着 image_mask 这张“X光片”，找到所有需要动手术的位置（值为True的地方），然后把这些位置上的旧组织（临时的占位向量）挖掉，再把 image_embeds 这个新的、充满活力的“视觉器官”植入进去。
        
    - **结果**: 手术完成后，inputs_embeds 这个序列里，原本是 <|image|> 占位符的地方，现在已经被一长串（比如256个）真正代表图片内容的视觉向量所取代。
        
3. **第三步：对视频进行同样的手术（如果存在）**
    
    codePython
    
    ````
    if pixel_values_videos is not None:
        # ... (逻辑和图片完全一样) ...
        inputs_embeds = inputs_embeds.masked_scatter(video_mask, video_embeds)
    ```    *   如果在序列里还有 `<|video|>` 占位符，就再做一次同样的手术，把视频特征向量也植入进去。
    ````
    

---

### 最终的成品

经过这一系列操作之后，inputs_embeds 就成了一个**真正的、无缝融合的多模态序列**。

它可能看起来像这样（概念上的）：

```

**[文本向量, ..., 文本向量] + [图片A的patch向量序列] + [文本向量, ...] + [视频B的patch向量序列] + [文本向量, ...]**
```


这个序列就是我们之前比喻的那个“**所有专家都在一个会议室里**”的状态。从这一刻起，对于下游的language_model来说，它再也分不清哪个是“原生”的文本信息，哪个是“植入”的视觉信息了。它看到的只是一个长长的、等待被处理的向量序列。