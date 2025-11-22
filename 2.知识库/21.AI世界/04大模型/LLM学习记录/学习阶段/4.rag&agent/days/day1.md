chatMessage:content和role 
首先，明白lanchain是个package，从python导入进来后，拥有许多module
# Model IO
接受用户输入，输出对话，langchain采用该模块集成到代码里，**封装各种语言模型的接口** ，使得开发者可以统一调用不同的模型
embedding、tokenizer，和输出是模型本身进行的哈
同时，此部分还有langchain自定义的一系列prompt方法