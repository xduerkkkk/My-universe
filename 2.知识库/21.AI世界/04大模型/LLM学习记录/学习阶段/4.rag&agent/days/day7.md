
```python
def get_unique_union(documents:list[list]): 
# Flatten list of lists, and convert each Document to string 
flattened_docs = [dumps(doc) for sublist in documents for doc in sublist] 
# Get unique documents 
unique_docs = list(set(flattened_docs)) 
# Return 
return [loads(doc) for doc in unique_docs]

```
生成了许多内容相同 但id不同的

LangChain 的 `dumps()` 方法会将整个 `Document` 对象转换成 JSON 字符串，但如果你的文档中包含以下字段之一：

|字段名|是否影响去重？|说明|
|---|---|---|
|`id`|✅ 是|每个`Document`自动生成唯一 ID，导致字符串不同|

```python
    # 只保留 page_content，忽略 metadata 和 id 差异

    seen = set()

    unique_docs = []

  

    for sublist in documents:

        for doc in sublist:

            content = doc.page_content

            if content not in seen:

                seen.add(content)

                unique_docs.append(doc)

  

    return unique_docs
```
`return [loads(doc) for doc in unique_docs]`才行


## fag fusion
排序

## decomposition
将问题拆解

## stepback
更抽象问题检索
1. **原始用户问题** ：
    
    - 比如：“为什么地球绕太阳转而不是反过来？”
2. **LLM 生成一个更抽象的问题（Step-Back Question）** ：
    
    - 比如：“行星是如何围绕恒星运行的？”
## HyDE
将答案替代问题 去检索

## Query Construction
直接rewrite prompt

```python
rewrite_prompt = PromptTemplate.from_template(
    "请将以下问题改写为更清晰、更适合知识库检索的形式：\n\n{question}"
)

rewrite_chain = rewrite_prompt | ChatOpenAI(model="gpt-3.5-turbo")
```
