 当我指定 model='hf' 和模型路径时，框架内部实际上是调用了 transformers 库的 AutoModel.from_pretrained() 和 AutoTokenizer.from_pretrained()。这也是为什么注册自定义模型如此重要的原因，因为它就是在这个环节让 transformers 认识我们的模型。
