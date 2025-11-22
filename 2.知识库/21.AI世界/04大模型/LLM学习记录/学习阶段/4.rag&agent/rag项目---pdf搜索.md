# 前端
关键在于
`requests.post()` 用于发起 HTTP POST 请求的函数**。
# 后端
前端的POST ，有两部分
第一部分：POST pDF文件
后端调用pdf_loader.py文件，解析并分块，传回后端，命名为chunks。后端再将分块的数据创建向量库。


此时后端可以用向量库了。

第二部分：POST ask，text文本
调用hybrid_search.py模块，此时检索需要用到刚才的向量库。
最后将检索的文本，当作上下文，调用generation.py模块，进行答案的生成。

# PDf_loader
切割为
{ 'page_content': '这是分割后的一段文本内容。', 'metadata': {...} # 其他元数据 }

# HybridFusionRetriever
```python
result = reasoning.answer(question)  # 内部会调用 retriever._get_relevant_documents
```

我们调用两次检索 

### **`all_results`的结构（示意）：**


```python

[   [doc1_q1, doc2_q1, doc3_q1],  # 关键词1的检索结果（按相关性排序）  
	[doc1_q2, doc2_q2, doc3_q2],  # 关键词2的检索结果    
	[doc1_q3, doc2_q3, doc3_q3],  # 关键词3的检索结果 ]

```
### **`reranked_docs`的结构（示意）：**


```python


[   docA,  # 最优排序的文档  
	docB,   
	docC,   #... ]
```

```python
self.ensemble = EnsembleRetriever(

            retrievers=[self.vector_retriever, self.bm25_retriever],

            weights=[

                self.config["retriever"]["vector_weight"],

                self.config["retriever"]["bm25_weight"]

            ]

        )
```

# Generation
from langchain.chains import RetrievalQA

RetrievalQA  

```
RetrievalQA.from_chain_type(

            llm=self.llm,

            chain_type="stuff",

            retriever=self.retriever,

            chain_type_kwargs={

                "prompt": PromptTemplate(

                    template=prompt_template,

                    input_variables=["context", "question"]

                )

            },

            return_source_documents=True
```


retriever=self.retriever能自动调用_get_relevant_documents方法