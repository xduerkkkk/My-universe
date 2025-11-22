## documentloader
langchain_community里导入
## text_splitter
langchain_text_splitters 导入
关键参数是separators，chunk_size, chunk_overlap
大模型里的chunksize是token，hello是一个token，但是textsplitter是字母！hello是五个
language=Language.PYTHON可以分割语言
semantic

.load方法（文件路径）后  为docs，此时是一个document对象
all_splits = text_splitter.split_documents(docs) 
之后的数据结构：多个document对象！ 

## embedding
embed_query和embed_document 都是传入字符串！
所以是传入all_split的content内容

## vector store
传入之前定义的embeddings_model 
用similarity_search 可以搜索语义相关的信息
## 向量库算法原理
### 暴力搜索
逐个寻找， 向量夹角或者欧几里得距离距离
### Approximate Nearest Neighbors
聚类，kmeans   局部敏感哈希（Locality Sensitive Hashing） LSH
### PQ
选聚类中的质心作为代表！略为 “失真” ，所以要高聚类。
把高维的分为低位的，低维的独立的聚类训练，最后把所有的结果拼接起来
例如一个 128 维的向量，需要维护 2^64 个聚类中心才能维持不错的量化结果，但这样的码本存储大小已经超过维护原始向量的内存大小了。
解决这个问题的方法是将向量分解为多个子向量，然后对每个子向量独立进行量化，比如将 128 维的向量分为 8 个 16 维的向量，然后在 8 个 16 维的子向量上分别进行聚类，因为 16 维的子向量大概只需要 256 个聚类中心就能得到还不错的量化结果，所以就可以将码本的大小从 2^64 降低到 8 * 256 = 2048 个聚类中心，从而降低内存开销。
实质是“维度”与“聚类中心”直接呈现，且只有指数关系，我们拆分后，引入了加法。
### Navigible Small Worlds
一个一个放点，每次都比如，强制连接3个相邻点。最终的图，又有长连接又有短链接。后面再查找某个向量时，使用先长后短
### Hierarchical Navigable Small Worlds (HNSW)
由长到短更加可观，更加平稳，更加出色

