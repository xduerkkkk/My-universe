# 第一遍，全局直觉
## Abstract&Instruction&配图
能接受文本图像视频音频 能输出文本音频
流式输出需要效率，为了效率音频和视觉编码器都采用分块处理
感知交给编码器  长序列建模交给llm
新技术：
- TMRoPE  为了同步视频输入的时间戳与印音频
- Thinker-Talker：Thinker作为llm负责文本生成，talker利用thinker生成音频
- Dit的滑动窗口：辅助生成语音

# 第二遍 深入骨架

## Perceivation
首先，我们的目的是将输入的所有模态，tokenizer化
- 音频：Qwen2-Audio（Chu 等人，2024b）中的音频编码器，使每个音频帧的表示大致对应于原始音频信号中的 40ms 片段
- 图片/视频（无音频）：Qwen2.5-VL（Bai 等人，2025）中的视觉编码器，该编码器基于视觉 Transformer（ViT）模型，参数量约为 6.75 亿，能够有效处理图像和视频输入
在他们tokenizer的基础上，还要加入TMRoPE 
针对音频是1d位置编码
图片是2d位置编码
视频是3d位置编码
取每一帧的**真实时间戳**，并把它换算成统一的40ms为单位的时间ID

## generation
Speech. Talker receives both high-level representations and embeddings of the text tokens sampled by
Thinker. The integration of high-dimensional representations and discrete sampling tokens is essential in
this context. As a streaming algorithm, voice generation must anticipate the content’s tone and attitude
before the entire text is fully generated. The high-dimensional representations provided by Thinker
implicitly convey this information, enabling a more natural streaming generation process. Furthermore,
Thinker’s representations primarily express semantic similarity in the representational space rather than
phonetic similarity. Consequently, even phonetically distinct words may have very similar high-level
representations, necessitating the input of sampled discrete tokens to eliminate such uncertainty.
We designed an efficient speech codec named qwen-tts-tokenizer. qwen-tts-tokenizer efficiently represents
key information of speech and can be decoded to speech streamingly through a causal audio decoder.
After receiving the information, Talker starts to autoregressively generate audio tokens and text tokens.
The generation of speech does not require word-level and timestamp-level alignment with the text. This
significantly simplifies the requirements for training data and the inference process.
语音完整生成前就要知晓语气，由llm生成的高维语义空间，传达了这个语气信息/。 

- - - Thinker在生成高维向量的同时，也会进行**采样 (sampling)**，明确地决定下一个词**就是**“开心”这个**离散的文本token** (token_id为 ...)
            
	- **最终，Talker会同时收到两份信息**：
		
		1. **高维表示 : 这份信息像“背景音乐”，告诉Talker当前对话的**整体情绪、语气和上下文**（比如是该用兴奋的语气，还是平静的语气）。这就是原文说的“传达语气信息”。
			
		2. **离散Token (sampled discrete tokens)**: 这份信息是**明确的指令**，告诉Talker：“别猜了，就给我说‘开心’这两个字！”
                
- **一句话总结**: **高维表示定“调调”（怎么说），离散Token定“词儿”（说什么）**


Furthermore,
Thinker’s representations primarily express semantic similarity in the representational space rather than
phonetic similarity. Consequently, even phonetically distinct words may have very similar high-level
representations, necessitating the input of sampled discrete tokens to eliminate such uncertainty.看不懂  
设计了一种名为 qwen-tts-tokenizer 的高效语音编解码器。The generation of speech 为什么？
- **旧”方法 (需要对齐)**: 以前做TTS（Text-to-Speech，文本转语音），需要非常“昂贵”的数据集。这种数据集不仅要有文本和对应的录音，还需要**精确地标注**出：文本里的“你”字，对应录音里 0.1s - 0.3s 的这段声音；“好”字，对应 0.3s - 0.5s 的声音... 这就是**词级和时间戳对齐**。制作这种数据集费时费力。
    
- **Qwen-Omni的“新”方法 (解耦)**:
    
    - 得益于Thinker-Talker架构，他们把这个过程**解耦 (decouple)** 了。
        
    - **训练时**: 他们只需要大量的 (文本, 对应的整段录音) 数据对。模型自己去学“这段话大概是这个声音”。它不需要知道哪个字对应哪段波形。Thinker学习理解语义，Talker学习把语义变成声音。
        
    - **推理时**:
        
        1. Thinker根据输入，生成它认为合适的**文本内容**（比如 "Hello world, how are you today?"）。
            
        2. Thinker把这些**文本内容**和对应的**高维表示**（包含了“应该用友好、疑问的语气”这类信息）传递给Talker。
            
        3. Talker接收到指令后，**独立地、流畅地**把 "Hello world, how are you today?" 这句话用友好、疑问的语气“说”出来。
            
    - Talker在生成语音时，会根据自己的“发声习惯”（模型参数）来决定语速、停顿。它不需要回头去问Thinker：“‘world’这个词我应该在第1.2秒说完吗？”。Thinker只管“内容”，Talker只管“表达”。
## Designs for Streaming
### Support Prefilling：
chunked prefill，不知道和之前学过的prefill有啥区别。然后prefill阶段flashattention，没问题，
	-  **传统Prefill**: **一次性**处理**全部**输入。
      
    - **Chunked Prefill**: **增量式、分块**处理输入流。
        
	- **好处**: 极大降低了初始响应的延迟。用户输入开始后很短的时间内（比如第一个块处理完），模型就可以开始生成响应，因为它已经有了初步的“理解”（KV Cache）。


### Streaming Codec Generation：
 DiT model辅助实现滑动注意力窗口
1. **Talker生成语音标记**: Talker是一个自回归模型，它一个接一个地生成**抽象的语音标记 (speech codec tokens)**。这些标记不是声音，而是声音的高度压缩表示。
    
2. **DiT声码器 (Vocoder)的角色**:
    
    - **任务**: 将这些抽象的语音标记**转换 (解码)** 成真实的声音波形 (waveform)。
        
    - **挑战**: 如何流式地进行转换？如果等Talker生成完100个标记，再用DiT一次性把它们转成声音，就会有延迟。
        
3. **DiT + 滑动窗口的解决方案**:
    
    - **滑动窗口 (Sliding Window)**: DiT在解码时，并不是看“所有已生成的语音标记”。它只关注一个**固定大小的、向前滑动的窗口**内的标记。
        
        - 比如，窗口大小为32。当要生成第50个时间点的声音波形时，DiT可能只看第18到50号语音标记。
            
        - 当要生成第51个时间点的声音波形时，窗口滑动，DiT就看第19到51号语音标记。
            
    - **DiT的作用**: 在这个滑动窗口内，DiT作为一个强大的条件生成模型，**高质量地预测**出下一个小段的声音波形。
        
    - **总结**: **滑动窗口**是一种**策略**，它告诉DiT“你应该看哪里”。而**DiT**是一个强大的**执行者**，它根据窗口内的信息，“画”出对应的声音。两者结合，使得声音的“渲染”过程可以和语音标记的生成过程**并行、流式**地进行，从而实现了极低的输出延迟。


- **输入端 (Prefill)**: 采用**分块处理 (Chunked Prefill)**，实现“边听边想”。
    
- **输出端 (Generation)**: 采用**滑动窗口+DiT声码器**的策略，实现“边想边说”。
## pretrain
Qwen2.5-Omni consists of three training stages. In the first stage, we lock the LLM parameters and focus
exclusively on training the vision encoder and audio encoder, utilizing a vast corpus of audio-text and
image-text pairs to enhance semantic understanding within the LLM. In the second stage, we unfreeze
all parameters and train with a wider range of multimodal data for more comprehensive learning. In
the final stage, we use data with a sequence length of 32k to enhance the model’s ability to understand
complex long-sequence data.
The model is pre-trained on a diverse dataset that includes various types such as image-text, video-text,
video-audio, audio-text and text corpus. We replace the hierarchical tags with the natural language
prompts following Qwen2-Audio (Chu et al., 2024a), which can improve better generalization ability and
better instruction following ability.
During the initial pre-training phase, the LLM component of Qwen2.5-Omni is initialized using the
parameters from Qwen2.5 (Yang et al., 2024b), while the vision encoder is the same as Qwen2.5-VL, and
the audio encoder is initialized with the Whisper-large-v3 (Radford et al., 2023). The two encoders are
trained separately on the fixed LLM, with both initially focusing on training their respective adapters
before training the encoders. This foundational training is crucial in equipping the model with a robust
understanding of core visual-textual and audio-textual correlations and alignments.
The second phase of pre-training marks a significant advancement by incorporating an additional 800
billion tokens of image and video related data, 300 billion tokens of audio related data, and 100 billion
tokens of video with audio related data. This phase introduces a larger volume of mixed multimodal data
and a wider variety of tasks, which enhances the interaction and deepens the understanding between
auditory, visual, and textual information. The inclusion of multimodal, multitask datasets is crucial for
developing the model’s ability to handle multiple tasks and modalities simultaneously, a vital capability
for managing complex real-world datasets. Moreover, pure text data plays an essential role in maintaining
and improving language proficiency.
To improve training efficiency, we limited the maximum token length to 8192 tokens in the previous
stages. Then, we incorporat long audio and long video data and extend the original text, audio, image,
and video data to 32,768 tokens for training. Experimental results indicate that our data shows significant
improvement in supporting long sequence data

1. training the vision encoder and audio encoder。和vl2.5一样，2.5是先训练vit。
2. unfreeze all parameters and train with a wider range of multimodal data 
3. use data with a sequence length of 32k to enhance the model’s ability to understand complex long-sequence data.
先训练感受模态，再训练模态与文本生成的配合，再训练长序列能力
和qwen2.5vl一样


## post train
介绍了Data Format 

```
<|im_start|>user
<|vision_start|>Video.mp4 [Two people are talking in the video]<|vision_end|>What are the
people in the video saying?<|im_end|>
<|im_start|>assistant
Both pictures are of SpongeBob SquarePants.The person in the red clothes says, "Hello, how’s
the weather today?" The person in the black clothes responds, "Hello, the weather is quite nice
today."<|im_end|>
<|im_start|>user
<|vision_start|>Video.mp4 [A person in the video is saying, "Please describe the person in front
of you."]<|vision_end|><|im_end|>
<|im_start|>assistant
The person in front of you is wearing glasses and a brown jacket over a blue shirt. They appear
to be speaking or reacting to something, as their mouth is open and they seem engaged. The
background shows a room with a wall-mounted air conditioner, a clothing rack with various
garments hanging on it, and a large screen displaying an image of a cityscape at night. The
lighting in the room is warm and cozy.<|im_end|>
```
应该就是展示tokenizer前的格式，方便人们自己制作微调的数据集？
后面介绍thinker的训练
During the post-training phase, we employ instruction-following data with ChatML (OpenAI, 2022)
format for instruction-finetuning. Our dataset incorporates pure text-based dialogue data, visual-modality
conversation data, audio-modality conversation data and mix-modality conversation data.
好像意思是传统的监督学习
然后是talker，有点难理解了
We introduced a three-stage training process for Talker, allowing Qwen2.5-Omni to generate text and
speech responses simultaneously. In the first stage, we train Talker to learn context continuation. The
second stage utilized DPO (Rafailov et al., 2023) to enhance the stability of speech generation. In the third
stage, we applied multi-speaker instruction fine-tuning to improve the naturalness and controllability of
the speech responses.
During the In-Context Learning (ICL) training phase, in addition to utilizing text supervision similar
to that of Thinker, we perform a speech continuation task through next-token prediction, leveraging
an extensive dataset of dialogues that incorporate multimodal contexts and spoken responses. Talker
learns to establish a monotonic mapping from semantic representation to speech, while also acquiring
the ability to express speech with diverse attributes that are contextually appropriate, such as prosody,
emotion, and accent. Additionally, we implement timbre disentanglement techniques to prevent the
model from associating specific voices with infrequent textual patterns.

To broaden the coverage of speakers and scenarios, the pretraining data inevitably contains label noise and
pronunciation errors, leading to model hallucinations. To mitigate this issue, we introduce a reinforcement
learning phase to improve the stability of speech generation. Specifically, for each request and response
text paired with the reference speech, we build a dataset D with the triplet data (x, yw, yl ), where x is
the input sequence with input text, and yw and yl are the good and bad generated speech sequences
respectively. We rank these samples based on their reward scores associated with word error rate (WER)
and the punctuation pause error rate.
Lastly, we performed speaker fine-tuning on the aforementioned base model, enabling Talker to adopt
specific voices and improve its naturalness

**第一阶段：学会“说话” (ICL / Context Continuation)**

- **目标**: 让Talker建立从**语义到声音**的基本映射，并学会根据上下文表达不同的**情感、韵律、口音**。
    
- **方法 (Next-token prediction)**: 这是一个**有监督的语音续写任务**。
    
    - **输入**: 一段对话的上下文（包含文字、图片、声音），以及这段对话对应的真人录音的**前一半**。
        
    - **目标**: 让Talker准确地预测出真人录音的**后一半**对应的语音标记是什么。
        
    - 通过海量的这种“语音填空题”，Talker就学会了：哦，原来在这样高兴的上下文里，说到“太棒了”这个词时，声音的韵律和音调应该是上扬的。
        
- **Timbre Disentanglement (音色解耦)**: 这是一个防止模型“学偏”的技术。比如，训练数据里某个罕见的词，恰好总是一个特定的人说的。模型可能会错误地认为“这个词就应该用这个人的声音说”。音色解耦技术就是为了打破这种错误的关联。
    

**第二阶段：把话说“对” (DPO / 稳定性增强)**

- **问题**: 预训练数据里有很多噪音（比如杂音、发音错误），导致模型在生成语音时可能会出现幻觉，比如口吃、说错词。
    
- **目标**: 提升语音生成的**稳定性 (stability)** 和**准确性 (accuracy)**。
    
- **方法 (DPO - 直接偏好优化)**: 这是你已经熟悉的技术了，但应用在了语音上。
    
    - **数据**: 构建 (输入x, 好的语音yw, 差的语音yl) 这样的偏好对。
        
    - **如何定义“好”/“差”**: 用一些客观指标来打分。比如：
        
        - **WER (Word Error Rate, 词错误率)**: 生成的语音转回文字后，和原始文本有多少个词不一样？错误率越低，语音越“好”。
            
        - **Punctuation Pause Error Rate (标点停顿错误率)**: 在逗号、句号的地方，停顿得对不对？
            
    - 通过DPO训练，模型会更倾向于生成那些WER低、停顿正确的“好”语音，从而变得更稳定、更不容易说错话。
        

**第三阶段：把话说“好” (Speaker Fine-tuning / 自然度与可控性)**

- **目标**: 让语音更**自然 (naturalness)**，并且能**模仿特定人的声音 (controllability)**。
    
- **方法**: 在前两个阶段训练好的通用模型基础上，用**高质量的、单一说话人**的数据进行微调。比如，用某个特定播音员的2小时录音来微调，就能得到一个能模仿这个播音员声音的模型。