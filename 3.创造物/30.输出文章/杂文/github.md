# Transformer from Scratch: A Deep Dive into the Core Mechanisms

欢迎来到【Transformer从零实现】项目。

本项目致力于从第一性原理出发，通过“理论文章”与“实践代码”相结合的方式，将独立的知识原子，锻造成一个逻辑清晰、洞见深刻的Transformer知识体系。我们相信，理解一个模型的最好方式，就是亲手将它实现出来。

---

## ✨ 项目理念

我们遵循三大核心理念：

*   **文码结合 (Article + Code):** 每一篇深度解析文章，都配有可运行、可复现的Jupyter Notebook代码，实现理论与实践的无缝对接。
*   **循序渐进 (Step-by-Step):** 我们不会直接将庞大的Transformer模型抛给你，而是沿着技术的演进脉络，从RNN的瓶颈开始，一步步揭示每个组件诞生的历史必然性。
*   **探究本质 (First Principles):** 我们鼓励“打开黑箱”。在关键模块（如Attention机制），我们将不仅仅是调用API，而是用最基础的张量运算亲手实现它，以确保最深刻的理解。

---

## 🗺️ 项目路线图 (Roadmap)

本项目将以“三部曲”的形式逐步完成。

### **第一部：变革前夜 —— RNN的瓶颈与Attention的曙光**

*   **📖 文章：** [**《为什么需要Transformer：从“词”的编码到“序列”的革命》**](你的文章链接)
    *   **状态:** ✅ 已发布
*   **💻 配套代码:**
    *   **状态:** ✅ 已完成
    *   **内容:**
        *   `01a_..._Demo.ipynb`: 通过代码生动复现静态词向量的“语序丢失”问题，并展示RNN如何从机制上解决它。包含一个【选读】部分，从零实现一个基础RNN。
        *   `01b_..._Application.ipynb`: 提供一个完整的工程范例，展示如何应用LSTM/RNN解决真实世界的情感分类任务。

### **第二部：核心引擎 —— 深入理解Self-Attention与Multi-Head Attention**

*   **📖 文章：** *(待发布)*
    *   **状态:** ⏳ 撰写中
*   **💻 配套代码:**
    *   **状态:** ⏳ 开发中
    *   **内容:** 从零实现Scaled Dot-Product Attention，并将其组装为Multi-Head Attention模块。

### **第三部：宏伟蓝图 —— 组装完整的Transformer Encoder-Decoder**

*   **📖 文章：** *(待发布)*
    *   **状态:** 🗓️ 规划中
*   **💻 配套代码:**
    *   **状态:** 🗓️ 规划中
    *   **内容:** 将所有零件组装起来，搭建一个可以运行的迷你Transformer模型。

---

## 🚀 如何开始 (Getting Started)

1.  **克隆本仓库:**
    ```bash
    git clone https://github.com/your_username/transformer-from-scratch.git
    cd transformer-from-scratch
    ```

2.  **创建并激活虚拟环境 (推荐):**
    ```bash
    python -m venv venv
    # Windows
    source venv/Scripts/activate
    # macOS / Linux
    source venv/bin/activate
    ```

3.  **安装依赖:**
    ```bash
    pip install -r requirements.txt
    ```
    *(注: `requirements.txt` 文件包含了运行所有Notebook所需的基础库，如PyTorch, numpy等。请根据你的代码实际使用的库来创建这个文件。)*

4.  **启动Jupyter Notebook:**
    ```bash
    jupyter notebook
    ```
    现在，你可以开始探索 `notebooks` 文件夹中的内容了！

---

## 👥 关于我们

本项目诞生于【LLM文章输出指挥室 (The Forge)】，由“工匠”负责构思与实现，“首席编辑”负责评审与打磨，旨在共同锻造公开发表水准的高质量技术作品。