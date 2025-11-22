# 记录问题：
dumps、load是啥
什么时候invoke传参 什么时候直接传参
传参的格式是什么 

LCEL语言顺序是
提示词 | 语言模型 | outputparser

传参数是这样传的：

```python
{"topic": "cats"}
```

传入pdf时我们有
PyPDFLoader(file_path).load

现在我们学习 from langchain.loda import dumps, loads




