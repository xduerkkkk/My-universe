# 邻接矩阵版本
仍然需要edges，仍然是点1，点2，权重，这样的结构
然后需要邻接矩阵，可以函数内初始化也可以函数外
但edges怎么滴也要传入函数，所以函数内最好了

minDIst数组，是指，节点距离源点，也就是start，的最近距离

```
def dijkstra(n,m,edges,start,end):
	初始化邻接矩阵
	初始化距离数组minDist，且minDist[start]为0
	初始化visited，全为False，【start】可以设True，也可以不，因为后面不会访问visited【start】的

	for循环，遍历所有节点： 最外层循环目的就是不依赖任何一个节点
		定义minval为无穷  # minval是一个中间量
		cur为-1         # cur是当前
		for v in range(1,n+1)： 第一次循环，
			一直遍历，找mindist最小的那个点，把它设置为当前节点，
		要遍历完才知道谁距离源点最小，所以在循环外，标记该节点被访问
		for v in range(1,n+1): 第二次循环
			我们已经找到与源点连接的新点了，
			那以这个点为桥梁，我们可以更新其他点到节点的距离：
			其他点是什么点？ 没visited ； grid【cur】【v】是有值的  ； 
			还有mindist【cur】 + grid【cur】【v】 小于minDist
			意思是，如果节点凭借新点，到源点的距离能更短的话，更新
			mindist【v】 = mindist【cur】 + grid【cur】【v】

	最后返回minDist【end】即可
			

```

# 邻接表版本
仍然需要edges，仍然是点1，点2，权重，这样的结构
然后需要邻接表，可以函数内初始化也可以函数外
但edges怎么滴也要传入函数，所以函数内最好了

对于邻接表的权重表示，直接用
```python
class Edge:
    def __init__(self, to, val):
        self.to = to
        self.val = val
```

注意，堆加入的元素，内容是
（cur_dist，cur_node)
```
def dijkstra
	先把grid定义咯
	grid[p1].append(Edge(p2,val))
	初始化距离数组minDist，且minDist[start]为0
	初始化visited，全为False，【start】可以设True，也可以不，因为后面不会访问visited【start】的
	初始化一个堆pq = 【】
	进行小顶堆的流程 heapq.headpush(pq,(0,start))

	while q：只要队列里还有候选节点，就继续处理
		把节点取出，heappop直接取出mindist最小的节点
		**if visited[cur_node]: continue**  如果visited还弹出了，这个肯定比最开始弹出那个弱 距离长

		弹出后，标记
		for edge in grid【取出的节点】：
			如果没访问，以及借助取出节点的桥梁能与源点更近的话
			更新mindist
			加入堆中

```
