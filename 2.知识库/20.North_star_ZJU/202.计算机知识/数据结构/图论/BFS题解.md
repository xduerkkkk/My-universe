# [200. 岛屿数量](https://leetcode.cn/problems/number-of-islands/)



![premium lock icon](https://static.leetcode.cn/cn-frontendx-assets/production/_next/static/images/lock-a6627e2c7fa0ce8bc117c109fb4e567d.svg)相关企业

给你一个由 `'1'`（陆地）和 `'0'`（水）组成的的二维网格，请你计算网格中岛屿的数量。

岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。

此外，你可以假设该网格的四条边均被水包围。

**示例 1：**

**输入：**grid = [
  ['1','1','1','1','0'],
  ['1','1','0','1','0'],
  ['1','1','0','0','0'],
  ['0','0','0','0','0']
]
**输出：**1

**示例 2：**

**输入：**grid = [
  ['1','1','0','0','0'],
  ['1','1','0','0','0'],
  ['0','0','1','0','0'],
  ['0','0','0','1','1']
]
**输出：**3


使用四个方向的BFS，看经历了多少次BFS，就有多少个岛屿
我们BFS的目标是  可以理解为淹没一个区域！
那我想，visited确实也可以在原grid里操作，把1改为0
BFS终止条件就是q没有新人了，说明一个区域掩完了。


```cpp
class Solution {

public:

    int numIslands(vector<vector<char>>& grid) {

        int n = grid.size();

        int m = grid[0].size();

        std::vector<std::vector<bool>> visited(n,std::vector<bool>(m,false));

        int dr[] = {-1,0,0,1};

        int dc[] = {0,-1,1,0};

        std::queue<std::pair<int,int>> q;

        int ans = 0;

        for(int i =0; i<n;i++)

        {

            for(int j=0; j<m; j++)

            {   if(!visited[i][j]&&grid[i][j]=='1')

                {q.push({i,j});

                    while(!q.empty())

                    {   auto [r,c] = q.front();

                        q.pop();

                        for(int k  = 0; k<4;k++)

                        {

                            int nr = r+dr[k];

                            int nc = c+dc[k];

                            if(nr>=0 && nr<n  && nc >= 0 && nc < m && !visited[nr][nc] && grid[nr][nc] =='1')

                            {

                                visited[nr][nc] = true;

                                q.push({nr,nc});

                            }

                        }

                    }

                    ans += 1;

                }

            }

        }

        return ans;

    }

};

```

更好的

```cpp
#include <vector>
#include <queue>

class Solution {
public:
    int numIslands(std::vector<std::vector<char>>& grid) {
        // 【前置检查】 - 保证代码鲁棒性
        if (grid.empty() || grid[0].empty()) {
            return 0;
        }

        int n = grid.size();
        int m = grid[0].size();
        std::vector<std::vector<bool>> visited(n, std::vector<bool>(m, false));
        int island_count = 0;

        // 【主循环】 - 遍历地图上的每一个点
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                // 【核心判断】 - 发现新岛屿的起点
                if (grid[i][j] == '1' && !visited[i][j]) {
                    // 1. 岛屿计数器加一
                    island_count++;
                    
                    // 2. 启动BFS来淹没/标记整个岛屿
                    bfs(grid, visited, i, j);
                }
            }
        }
        return island_count;
    }

private:
    // 【辅助函数】 - BFS模块，负责从一个点开始淹没一个岛屿
    void bfs(const std::vector<std::vector<char>>& grid, 
             std::vector<std::vector<bool>>& visited, 
             int start_r, int start_c) {
        
        int n = grid.size();
        int m = grid[0].size();
        std::queue<std::pair<int, int>> q;

        q.push({start_r, start_c});
        visited[start_r][start_c] = true;

        int dr[] = {-1, 1, 0, 0}; // 4个方向
        int dc[] = {0, 0, -1, 1};

        while (!q.empty()) {
            auto [r, c] = q.front();
            q.pop();

            for (int i = 0; i < 4; ++i) {
                int nr = r + dr[i];
                int nc = c + dc[i];

                // 检查邻居的合法性
                if (nr >= 0 && nr < n && nc >= 0 && nc < m && 
                    grid[nr][nc] == '1' && !visited[nr][nc]) {
                    
                    visited[nr][nc] = true;
                    q.push({nr, nc});
                }
            }
        }
    }
};

```


# [752. 打开转盘锁](https://leetcode.cn/problems/open-the-lock/)

中等

相关标签

![premium lock icon](https://static.leetcode.cn/cn-frontendx-assets/production/_next/static/images/lock-a6627e2c7fa0ce8bc117c109fb4e567d.svg)相关企业

提示

你有一个带有四个圆形拨轮的转盘锁。每个拨轮都有10个数字： `'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'` 。每个拨轮可以自由旋转：例如把 `'9'` 变为 `'0'`，`'0'` 变为 `'9'` 。每次旋转都只能旋转一个拨轮的一位数字。

锁的初始数字为 `'0000'` ，一个代表四个拨轮的数字的字符串。

列表 `deadends` 包含了一组死亡数字，一旦拨轮的数字和列表里的任何一个元素相同，这个锁将会被永久锁定，无法再被旋转。

字符串 `target` 代表可以解锁的数字，你需要给出解锁需要的最小旋转次数，如果无论如何不能解锁，返回 `-1` 。

**示例 1:**

**输入：**deadends = ["0201","0101","0102","1212","2002"], target = "0202"
**输出：**6
**解释：**
可能的移动序列为 "0000" -> "1000" -> "1100" -> "1200" -> "1201" -> "1202" -> "0202"。
注意 "0000" -> "0001" -> "0002" -> "0102" -> "0202" 这样的序列是不能解锁的，
因为当拨动到 "0102" 时这个锁就会被锁定。

**示例 2:**

**输入:** deadends = ["8888"], target = "0009"
**输出：**1
**解释：**把最后一位反向旋转一次即可 "0000" -> "0009"。

**示例 3:**

**输入:** deadends = ["8887","8889","8878","8898","8788","8988","7888","9888"], target = "8888"
**输出：**-1
**解释：**无法旋转到目标数字且不被锁定。



这确实有点抽象了
这怎么画图？ 我又不可能画一个四维的图
嗯，我们要表示出状态转移 
我突然想的是，邻接表，比如 0 的邻居 是 1和9     9的邻居是8和0 
0到8要几步？ 就是邻接表跳了几次，两次。
额， 跟这个题有什么关系？
好像也不够啊，比如0102是锁，那怎么表示？ 
等等，把题目数字缩短为两位，我发现二维图很清晰
比如  22  他能到哪去？  12  23 21 32  诶， 这不就是BFS图的四个方位吗   额，但是12  到92 这种情况又咋表示
emm 反正 难道我真的用四维数组？
存储量也爆炸吧 

我们用一个代码就把邻居遍历完





```cpp
class Solution {

public:

    int openLock(vector<string>& deadends, string target) {

        std::unordered_set<std::string> dead_set(deadends.begin(), deadends.end());

  

        // 【边界条件检查】 - 如果起点或终点在死亡列表里

        if (dead_set.count("0000")) {

            return -1;

        }

        if (target == "0000") {

            return 0;

        }

  

        // 【核心数据结构】

        std::queue<std::string> q;

        std::unordered_set<std::string> visited;

  

        // 【设置起点】

        q.push("0000");

        visited.insert("0000");

        int steps = 0;

  

        while(!q.empty())

        {  

            steps++;

            int level_size = q.size();

            for(int i =0;i<level_size;i++)

            {

                std::string current_lock = q.front();

                q.pop();

                for(int j =0; j<4; j++)

                {

                    char original_char = current_lock[j];

                    current_lock[j] = (original_char == '9') ? '0' : original_char + 1;

                    if (current_lock == target) return steps;

                    if (!dead_set.count(current_lock) && !visited.count(current_lock)) {

                        q.push(current_lock);

                        visited.insert(current_lock);

                    }

  

                    // 向下转动一次 (基于原始状态)

                    current_lock[j] = (original_char == '0') ? '9' : original_char - 1;

                    if (current_lock == target) return steps;

                    if (!dead_set.count(current_lock) && !visited.count(current_lock)) {

                        q.push(current_lock);

                        visited.insert(current_lock);

                    }

  

                    // 恢复，以便处理下一位

                    current_lock[j] = original_char;

                }

            }

  

        }

        return -1;

  

    }

};

```



# [127. 单词接龙](https://leetcode.cn/problems/word-ladder/)


字典 `wordList` 中从单词 `beginWord` 到 `endWord` 的 **转换序列** 是一个按下述规格形成的序列 `beginWord -> s1 -> s2 -> ... -> sk`：

- 每一对相邻的单词只差一个字母。
-  对于 `1 <= i <= k` 时，每个 `si` 都在 `wordList` 中。注意， `beginWord` 不需要在 `wordList` 中。
- `sk == endWord`

给你两个单词 `beginWord` 和 `endWord` 和一个字典 `wordList` ，返回 _从 `beginWord` 到 `endWord` 的 **最短转换序列** 中的 **单词数目**_ 。如果不存在这样的转换序列，返回 `0` 。

 

**示例 1：**

**输入：**beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
**输出：**5
**解释：**一个最短转换序列是 "hit" -> "hot" -> "dot" -> "dog" -> "cog", 返回它的长度 5。

**示例 2：**

**输入：**beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
**输出：**0
**解释：**endWord "cog" 不在字典中，所以无法进行转换。


其实和转盘锁很像了，
问题是， 转盘锁的“转”  是一个数字，+- 1  很简单
但现在是一个字母 可以往其余25个字母变啊 
如示例1 hit  是起点   他下一步能搜索到的邻居 有 25乘3个这么多吧？
哦 我们忽视了wordlist 也许wordlist不应该只是一个检测工具  最开始搜索邻居的时候就应该用wordlist做限制？ 
然后还得有visited 
如果一直拿hit做bfs复杂度很恐怖
那我们用终点cog和他双向奔赴一下  
最短路径就是  二者相遇？ 即探索出共同的邻居时  俩者探索层数和即为路径？

```cpp
#include <string>
#include <vector>
#include <queue>
#include <unordered_set>
#include <unordered_map>

class Solution {
public:
    int ladderLength(std::string beginWord, std::string endWord, std::vector<std::string>& wordList) {
        // 1. 将 wordList 放入哈希集合，便于O(1)查询
        std::unordered_set<std::string> wordSet(wordList.begin(), wordList.end());
        if (wordSet.find(endWord) == wordSet.end()) {
            return 0; // 优化：如果终点不存在，直接返回
        }

        // 2. 初始化双向BFS的数据结构
        std::queue<std::string> q_start, q_end;
        std::unordered_map<std::string, int> visited_start, visited_end;

        q_start.push(beginWord);
        visited_start[beginWord] = 1; // 路径长度从1开始计数

        q_end.push(endWord);
        visited_end[endWord] = 1;

        // 3. 双向BFS主循环
        while (!q_start.empty() && !q_end.empty()) {
            // 优化：优先扩展节点数少的队列
            if (q_start.size() <= q_end.size()) {
                if (extendQueue(q_start, visited_start, visited_end, wordSet) != -1) {
                    return extendQueue(q_start, visited_start, visited_end, wordSet);
                }
            } else {
                if (extendQueue(q_end, visited_end, visited_start, wordSet) != -1) {
                    return extendQueue(q_end, visited_end, visited_start, wordSet);
                }
            }
        }
        
        return 0; // 无法到达
    }

private:
    // 辅助函数，负责扩展一层队列
    int extendQueue(std::queue<std::string>& q,
                      std::unordered_map<std::string, int>& visited_self,
                      std::unordered_map<std::string, int>& visited_other,
                      std::unordered_set<std::string>& wordSet) {
        
        int level_size = q.size();
        for (int i = 0; i < level_size; ++i) {
            std::string word = q.front();
            q.pop();
            int current_dist = visited_self[word];

            // 生成所有邻居
            for (int j = 0; j < word.length(); ++j) {
                char original_char = word[j];
                for (char c = 'a'; c <= 'z'; ++c) {
                    word[j] = c;
                    
                    // 检查是否在wordList中
                    if (wordSet.count(word)) {
                        // 检查是否与另一端相遇
                        if (visited_other.count(word)) {
                            return current_dist + visited_other[word];
                        }

                        // 检查是否是己方未访问过的节点
                        if (!visited_self.count(word)) {
                            visited_self[word] = current_dist + 1;
                            q.push(word);
                        }
                    }
                }
                word[j] = original_char; // 恢复
            }
        }
        return -1; // 本轮未相遇
    }
};


```
# [1293. 网格中的最短路径](https://leetcode.cn/problems/shortest-path-in-a-grid-with-obstacles-elimination/)

困难

相关标签

![premium lock icon](https://static.leetcode.cn/cn-frontendx-assets/production/_next/static/images/lock-a6627e2c7fa0ce8bc117c109fb4e567d.svg)相关企业

提示

给你一个 `m * n` 的网格，其中每个单元格不是 `0`（空）就是 `1`（障碍物）。每一步，您都可以在空白单元格中上、下、左、右移动。

如果您 **最多** 可以消除 `k` 个障碍物，请找出从左上角 `(0, 0)` 到右下角 `(m-1, n-1)` 的最短路径，并返回通过该路径所需的步数。如果找不到这样的路径，则返回 `-1` 。

**示例 1：**

![](https://pic.leetcode.cn/1700710956-kcxqcC-img_v3_025f_d55a658c-8f40-464b-800f-22ccd27cc9fg.jpg)

**输入：** `grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]], k = 1`
**输出：** 6
**解释：** 
不消除任何障碍的最短路径是 10。
消除位置 (3,2) 处的障碍后，最短路径是 6 。该路径是 `(0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2) -> **(3,2)** -> (4,2)`.

**示例 2：**

![](https://pic.leetcode.cn/1700710701-uPqkZe-img_v3_025f_0edd50fb-8a70-4a42-add0-f602caaad35g.jpg)

**输入：** ` grid = [[0,1,1],[1,1,1],[1,0,0]], k = 1`
**输出：** -1
**解释：** 我们至少需要消除两个障碍才能找到这样的路径。



这题有点狠  我觉得，难点在于，如何让机器自己决策，是否消耗cost。
嗯，遍历所有可能的情况，选择最优的？
比如说， 第一个例子，k=1。 那就挨个障碍物消除试试，每次都在一个”新地图“进行bfs看最短路径。
但这样似乎复杂度很高啊 诶？复杂度是多少  一次bfs 时间复杂度是？ 呀 怎么分析 都不会了 是o(n)吧？ 队列里面最多就塞n个节点吧  。 然后我们 如果k=1，障碍物很多的话，我们重构地图，甚至要到o（n方）的复杂度吧？
但我想不出其他的，先顺着这个思路想。 那就是正常bfs  遇到一个障碍物就消耗一次k 我们试着打破一下  但，为了其他情况的出现，我们还要还原一下，然后visited刚才的操作，继续找其他的障碍物试图打破。不过刚才我们第一个打破障碍物的bfs，仍在继续探索中。呃，这一个队列够吗？够吧？感觉只要把visited逻辑处理好就行了？

模拟一下 nr,nc 
- 首先要在边界里
- 像常规bfs一样，若k相同的情况下 visit过 不行
没碰到障碍物 那无事发生 看看是不是终点 否则继续
碰到障碍物 看看k够不够 够的话击碎 看看是不是终点  否则 ”平行时空“前进 







# [1368. 使网格图至少有一条有效路径的最小代价](https://leetcode.cn/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/)



给你一个 m x n 的网格图 `grid` 。 `grid` 中每个格子都有一个数字，对应着从该格子出发下一步走的方向。 `grid[i][j]` 中的数字可能为以下几种情况：

- **1** ，下一步往右走，也就是你会从 `grid[i][j]` 走到 `grid[i][j + 1]`
- **2** ，下一步往左走，也就是你会从 `grid[i][j]` 走到 `grid[i][j - 1]`
- **3** ，下一步往下走，也就是你会从 `grid[i][j]` 走到 `grid[i + 1][j]`
- **4** ，下一步往上走，也就是你会从 `grid[i][j]` 走到 `grid[i - 1][j]`

注意网格图中可能会有 **无效数字** ，因为它们可能指向 `grid` 以外的区域。

一开始，你会从最左上角的格子 `(0,0)` 出发。我们定义一条 **有效路径** 为从格子 `(0,0)` 出发，每一步都顺着数字对应方向走，最终在最右下角的格子 `(m - 1, n - 1)` 结束的路径。有效路径 **不需要是最短路径** 。

你可以花费 `cost = 1` 的代价修改一个格子中的数字，但每个格子中的数字 **只能修改一次** 。

请你返回让网格图至少有一条有效路径的最小代价。

**示例 1：**

![](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2020/02/29/grid1.png)

**输入** grid = `[[1,1,1,1],[2,2,2,2],[1,1,1,1],[2,2,2,2]]`
**输出** 3
**解释：** 你将从点 (0, 0) 出发。
到达 (3, 3) 的路径为： (0, 0) --> (0, 1) --> (0, 2) --> (0, 3) 花费代价 cost = 1 使方向向下 --> (1, 3) --> (1, 2) --> (1, 1) --> (1, 0) 花费代价 cost = 1 使方向向下 --> (2, 0) --> (2, 1) --> (2, 2) --> (2, 3) 花费代价 cost = 1 使方向向下 --> (3, 3)
总花费为 cost = 3.