
```
初始化edges ： 点1，点2，权值
初始化minDist   除了minDist【1】为0外其他都是无穷大

for循环 最多遍历n-1次：
	updated = False  用于提前打断循环，如果不更新了，那就得到结果了，不用再费时间循环了
	for循环 遍历每个边：
		对每个边进行松弛操作
		即 if minDist【点1】 ！= 无穷 且 mindist【点1】+weight < mindist【点2】
		意思是如果点2以点1为桥梁，能距离源点更近的话
		更新mindist【点2】 = mindist【点1】 + weight
```
为什么遍历n-1次呢，其实这个算法也不知道到底遍历多少次，我就能找到最短路径，他只知道最坏情况下，就遍历n-1次，所以把总次数设立为n-1.中途不update了再跳出就行。

所以我们遍历次数大于n，和遍历n-1次，得到的结果是一模一样的。
但是！ 若图中有负权回路，那就会变小。所以可以通过第n次遍历，比较第n-1次遍历，判断图中是否有负权回路

# SPFA

```python
minDist = [float("inf")] * (n + 1) 
minDist[1] = 0 
que = collections.deque([1]) 
visited = [False] * (n + 1) 
visited[1] = True 
while que: 
	cur = que.popleft() 
	visited[cur] = False 
	for dest, weight in edges[cur]: 
		if minDist[cur] != float("inf") and minDist[cur] + weight < minDist[dest]:             minDist[dest] = minDist[cur] + weight 
			if visited[dest] == False: 
				que.append(dest) 
				visited[dest] = True

```
