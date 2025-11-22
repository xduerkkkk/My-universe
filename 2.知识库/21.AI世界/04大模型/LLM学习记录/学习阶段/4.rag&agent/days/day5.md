接着昨天的
vectorstore是定义好的数据库的话
回忆一下昨天是，vectorstore.similarity_search(“用户提示词”) 返回语义相近的语句

今天学到的就是添加智能了！  方法是 retriever = vectorstore.as_retriever() ，用来检索  使用方法是retriver.invoke(句子)
format_doc 把文章格式化为字符串
RunnablePassthrough()表示原样传递输入问题


```python

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
    
rag_chain = (
	{'context':retriver | format_docs, "question" : RunnablePassthrough()}
	| prompt
	| llm
	| strOutputParser()
)

```
昨天学了openaiembedding或其他模型
今天学习用tiktoken模块

```python
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")  # 本地加载编码器
tokens = encoding.encode("你好，世界！")           # 本地编码
```
