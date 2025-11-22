# 基础使用
vllm有两种方式部署模型，将模型打包成一个服务。
一种是本地部署，属于线下服务
一种是api方式部署，属于线上服务
用到的内核，一个是LLMEngine，一个是AsyncLLMEngine
两种都是continues batching  ，有waiting running队列，一直动态变化。
只不过对于线下，调用者和被调用者在**同一个进程/线程**，所以称“同步”
对于线上，调用者和服务器在**两个独立进程**，所以称“异步”

# 核心思想

vllm能高效得将大模型包装成服务，靠的是核心思想pagedattention。
如果直接在物理块上存储数据，
1. 必须要连续，不连续就找不见了嘛。==传统的内存分配方式，要求为**一个完整的序列**预留**一整块巨大的、物理上连续的**显存空间。这么做的主要原因，是为了**GPU访问的高效性**。GPU尤其擅长处理大块的、连续的数据（Coalesced Memory Access）==。
2. 不知道你到底会占用多少，因为大模型生成是不可控长度的。这个预分配不知道如何解决
我们引入逻辑块，每个逻辑块对应一个物理块，这样我们不关心物理连续不连续。只要逻辑连续，顺着逻辑块找，就算物理不连续也没关系，我们丢不了数据。同时，还可以节省资源：先给你一块，不够了再给你一块，够了就ok，不再给了。
一个逻辑块，可以说有多个格子，一个格子一个token_id。 逻辑块所包含的属性，除了检查自身格子外，还有将tokenid安装到自己的格子上的方法。

# generate
定义一个llm类，就相当于部署一个大模型了。
使用generate函数，就能给用户返回结果了

```
llm = LLM(model=...)
output = llm.generate(...)

```
所以我们进入generate看看，里面有什么奇妙的地方
最核心的就是，
```python
self._add_request

self._run_engin

```
其中，在看看_add_request是啥，发现调用的是
```python3
self.llm_engine.add_request
```
_runegnin_呢 用的是
```python3
self.llm_engine.step()
```

所以核心的核心，就是llmengine，它下面的这两个函数
# LLMEngine

就两个函数，
- add_request():登记客人，在这里就把客人信息打包好（包装成sequence，形成sequence_group)
- step(): 执行一次完整的流程，在最初的版本里，是prefill和decoding二选一。

首先讲一下怎么把客人信息打包的， 客人基础信息其实就是prompt，先包装成一个sequence，
有两个个重要属性和一个方法
两个属性
- self.status:是waiting的未来的新顾客呢，还是running的老顾客呢，还是空间不足，swapped的倒霉老顾客呢
- self.logical_token_blocks: 记录prompt，去存储的逻辑块id
一个方法
- append_tokens_to_blocks方法：还记得逻辑块自身有方法吗

```
 逻辑块所包含的属性，除了检查自身格子外，还有将tokenid安装到自己的格子上的方法。
```
我们seq，是有着自己的逻辑块名单的，当Sequence需要添加新token时，它会调用**它自己**的_append_tokens_to_blocks方法。这个方法**内部**，会去检查logical_token_blocks列表里的**最后一个**LogicalTokenBlock对象的状态（比如is_full()）， 然后，它会调用那个LogicalTokenBlock对象的append_tokens方法，把token ID“写”进去。

那seq_group是啥呢？ 就是专门应对beamsearch和parallel sampling，他们的要求是同一个prompt，多个output，索性把这些prompt（都一样）和output都包装起来，方便管理。


剩下关于系统运转的一切细节，就蕴含在step函数里

step函数还要传入
- **`max_num_seqs`**：在1个推理阶段中，LLMEngine最多能处理的seq数量（1条seq就是指我们待推理的1条数据）。默认是256
- **`max_num_batched_tokens`**：在1个推理阶段中，LLMEngine最多能处理的token数量。默认是2048
这两个数据，到底谁在用，是step里面小弟的事。

# step函数的出场角色
管理层
- Scheduler：调度者，他负责检查所有客人，所有seq_g 不论是新客人还是老客人。经过一系列复杂的判断后，得到一个名单，上面记录要服务的对象，和其他记录性的信息。这个名单给谁？是**统一**返回给LLMEngine.step()函数的。LLMEngine再根据名单上的prompt_run标志，决定指挥Worker是进行Prefill还是Decoding 
- BlockManager：检查整个空间，向上层Scheduler提供**查询接口**，如can_allocate和can_append_slot，还能呼叫执行者blockAllocator去做事，让他用自己的能力allocate或free
- Executor：管理所有works，是单卡还是多卡，是什么分布式框架等。
执行层：
- BlockAllocator：实际参与分配物理块的执行者。分为uncache的和cache的，一个老实一个聪明。uncache就是来一个客人就分配一个物理房间，cache的会去检查是否能共享资源，还有之前用过的现在能不能用到
- Worker：两把武器，一个是cacheengine，管理物理块的数据，**执行**由Scheduler和BlockManager制定的**内存操作指令**，一个是worker.model，进行前向传播，推理，是最底层的执行者。模型权重也是最开始在这里加载的。

**FCFS**调度原则、 **Preemption**、**带有冷却时间的Prefill优先**、**LRU缓存淘汰**机制

### 理解那个最重要的结论

> “在1个推理阶段中，所有的seq_group要么全部处在prefill阶段。要么全部处在decode阶段。”

### 从“决策”到“执行”的精确时间线

我们来扮演一次LLMEngine，完整地走一遍step()函数处理**一个新请求**的流程。

**时间点 T0：llm_engine.step() 被调用**

1. **进入Scheduler._schedule()**：引擎把控制权交给了“参谋长”（Scheduler）。
    
2. **调度器开始决策（_schedule函数内部）**：
    
    - 参谋长发现swapped队列为空。很好，可以考虑接纳新人。
        
    - 他开始审查waiting队列的队头，那个我们称之为SG_A的新请求。
        
    - 他对其进行**“四重安检”**：
        
        1. 检查prompt_limit -> 通过。
            
        2. 调用self.block_manager.can_allocate(SG_A) -> **此时，第一次和BlockManager交互！** BlockManager只进行**查询**，告诉他OK。
            
        3. 检查max_num_batched_tokens -> 通过。
            
        4. 检查max_num_seqs -> 通过。
            
    - **决策完成！** SG_A通过了所有安检。
        
    - 参谋长现在**更新他的内部状态**：
        
        - self.waiting.popleft()：把SG_A从等待队列移除。
            
        - self.running.append(SG_A)：**在逻辑上**，把SG_A加入到“即将运行”的队列中。
            
        - scheduled.append(SG_A)：把SG_A记录到本次的“行动清单”里。
            
    - **【关键】分配物理块的指令下达！**
        
        - self._allocate(SG_A)：参谋长对“酒店总管”(BlockManager)下达了一个**命令**：“去，为SG_A这个新客人，把房间都准备好！”
            
3. **块管理器开始执行（BlockManager.allocate()内部）**：
    
    - **此时，才真正开始物理块的分配！**
        
    - 酒店总管拿到命令，开始遍历SG_A的所有逻辑块。
        
    - 他不断地调用底层的self.gpu_allocator.allocate()，从空闲池里**实际地取出**一个个物理块。
        
    - 他把取出的物理块地址，一一填写到SG_A的BlockTable（索引卡片）里。
        
    - **分配完成！** allocate()函数执行完毕，返回。
        
4. **调度器完成工作**：
    
    - _schedule函数打包好SchedulerOutputs对象（里面包含了scheduled列表，prompt_run=True等信息），然后return。
        
    - “参谋长”的工作结束了。
        

**时间点 T1：控制权回到LLMEngine**

1. **引擎拿到“行动计划书”**：LLMEngine拿到了Scheduler返回的SchedulerOutputs。
    
2. **引擎命令“开火”**：
    
    - LLMEngine把这份计划书，交给底层的model_runner（“前线部队”）。
        
    - model_runner看到prompt_run=True，并且scheduled列表里有SG_A。
        
    - 它就知道，这次要对SG_A执行**Prefill**操作。
        
    - 它会根据SG_A的BlockTable，找到那些**刚刚被分配好**的物理块的地址，然后调用CUDA Kernel，开始进行矩阵乘法