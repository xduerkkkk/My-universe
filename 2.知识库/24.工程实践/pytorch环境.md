# 俩个版本
cpu版本和gpu版本
完全是不同的编译包

# 版本号进化

PyTorch作为一个活跃的开源深度学习框架，其版本迭代反映了功能的增强、性能的优化以及对新技术（如新的CUDA版本、Python版本）的支持。

- **早期版本 (小于1.0.0):** Facebook最初将Python和Torch库结合，创造了这个开源框架，支持在NVIDIA GPU上使用CUDA进行加速。这个阶段的版本奠定了PyTorch以张量（Tensors）为核心，进行多维数组存储和操作的基础。
    
- **1.x 版本:** 这一系列的版本带来了许多重要更新，例如对Windows的支持，以及引入了ONNX（开放神经网络交换）以便于在不同框架间转换模型
**PyTorch 2.0及以后:** 这是一个里程碑式的版本，引入了torch.compile，一个通过模型编译来大幅提升性能的新特性，使得模型训练速度更快，同时保持了PyTorch一贯的Python风格和动态性PyTorch 2.0的设计是100%向后兼容的，旨在为用户提供更快的性能和对动态形状、分布式训练的更好支持

# CUDA
**CUDA (Compute Unified Device Architecture)** 是由NVIDIA（英伟达）推出的一个**并行计算平台和编程模型**。

您的理解“是英伟达专门配套的编译语言”对了一部分，但CUDA远不止于此。它是一个完整的生态系统，主要包含三个层面：

1. **硬件层面**：指的是NVIDIA的GPU（显卡）。只有NVIDIA的GPU才拥有CUDA核心，可以执行CUDA程序。
    
2. **软件层面 (核心)**：这是一套完整的软件开发工具包（**CUDA Toolkit**）。它包含了：
    
    - **CUDA编译器**：比如nvcc，它能编译C/C++语言的扩展（CUDA C/C++），让程序员可以直接编写在GPU上运行的代码。
        
    - **CUDA库**：一系列高度优化的库，用于执行特定任务，例如：
        
        - cuBLAS：用于线性代数计算。
            
        - cuFFT：用于快速傅里叶变换。
            
        - cuDNN：专门为深度神经网络设计的加速库，PyTorch、TensorFlow等框架都严重依赖它。
            
    - **CUDA驱动**：安装在操作系统中，让CPU能够与GPU通信并下达指令的底层软件。
        
3. **应用层面**：像PyTorch这样的深度学习框架，其GPU版本内部就大量调用了CUDA库（特别是cuDNN和cuBLAS），将张量计算（如矩阵乘法）从CPU转移到GPU上，利用GPU数千个核心的并行处理能力，实现数十倍甚至上百倍的加速。
    

**总结：** 您可以把GPU想象成一个拥有数千名工人的大型工厂，而CPU是只有几个核心专家的办公室。CUDA就是这套工厂的管理体系、生产工具和操作手册，它让您（通过PyTorch）能够将大规模、可并行的计算任务（比如训练模型）高效地分配给这数千名工人去同时完成。


### 查看电脑的CUDA
`nvidia-smi`
我们安装的pytorch-cuda 要低于上面显示的版本
conda create -n gpu python=3.11 pytorch torchvision torchaudio pytorch-cuda=12.1 
-c pytorch -c nvidia
# 出现问题
pip torch时
ERROR: No matching distribution found for torch

conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
