```python
def dfs(整个图，当前节点，辅助存储答案的结构)：
	处理当前节点
	遍历该节点的邻居，
	即for neighbor in graph【node】：
		dfs（）  递归处理
```


```cpp
void dfs(int u, std::vector<std::vector<int>>& graph, std::vector<bool>& visited)
{
	visited[u] = true;
	//process(u);
	for(int v: graph[u])
	{
		if(!visited[v])
		{
			dfs(v,graph,visited);
		}
	}
}

```


