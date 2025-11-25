# [695. 岛屿的最大面积](https://leetcode.cn/problems/max-area-of-island/)

给你一个大小为 `m x n` 的二进制矩阵 `grid` 。

**岛屿** 是由一些相邻的 `1` (代表土地) 构成的组合，这里的「相邻」要求两个 `1` 必须在 **水平或者竖直的四个方向上** 相邻。你可以假设 `grid` 的四个边缘都被 `0`（代表水）包围着。

岛屿的面积是岛上值为 `1` 的单元格的数目。

计算并返回 `grid` 中最大的岛屿面积。如果没有岛屿，则返回面积为 `0` 。

**示例 1：**

![](https://assets.leetcode.com/uploads/2021/05/01/maxarea1-grid.jpg)

**输入：**grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
**输出：**6
**解释：**答案不应该是 `11` ，因为岛屿只能包含水平或垂直这四个方向上的 `1` 。


缝缝补补，毫无章法版 
```cpp
class Solution {

private:

    int dfs(vector<vector<int>>& grid,std::pair<int,int> aim,int cols, int rows)

    {   auto [r,c] = aim;

        int m=0;

        int dr[] = {-1,0,0,1};

        int dc[] = {0,-1,1,0};

        for(int i=0;i<4;i++)

        {

            int nr = r+dr[i];

            int nc = c+dc[i];

            if(0<=nc&&nc<cols&&0<=nr&&nr<rows&&grid[nr][nc]==1)

            {  

                grid[nr][nc] = 0;

                m += dfs(grid, {nr, nc}, cols, rows);

                }

        }

        return 1+m;

    }

public:

    int maxAreaOfIsland(vector<vector<int>>& grid) {

  

        int rows = grid.size();

        int cols = grid[0].size();

  

        int ans = 0;

        for(int i=0; i<rows;i++)

        {

            for(int j=0; j<cols; j++)

            {

                if(grid[i][j]==1)

                {   grid[i][j]=0;

                    ans = std::max( ans,dfs(grid,{i,j},cols,rows));

                }

            }

        }

        return ans;

    }

};

```

标准版本
递归责任下放！而不是“保姆式递归”。
在递归函数中，一开始，就检测是否为水域/越界


```cpp
#include <vector>
#include <algorithm> // for std::max

class Solution {
public:
    int maxAreaOfIsland(std::vector<std::vector<int>>& grid) {
        int n = grid.size();
        int m = grid[0].size();
        int max_area = 0;

        // 遍历每一个点
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                // 只有遇到陆地 '1' 才触发 DFS
                if (grid[i][j] == 1) {
                    // DFS 返回该岛屿的面积，更新最大值
                    max_area = std::max(max_area, dfs(grid, i, j));
                }
            }
        }
        return max_area;
    }

private:
    // DFS函数：返回从 (r, c) 开始的连通区域面积
    int dfs(std::vector<std::vector<int>>& grid, int r, int c) {
        // 1. 【Base Case / 终止条件】
        // 如果越界，或者是水域 (0)，直接返回 0
        // 注意：grid.size() 这种在频繁递归中调用可能会稍慢，
        // 追求极致性能可以传参 n 和 m，但这里为了代码清晰先这样写。
        if (r < 0 || r >= grid.size() || c < 0 || c >= grid[0].size() || grid[r][c] == 0) {
            return 0;
        }

        // 2. 【标记访问】
        // 将当前陆地淹没（变为0），防止回头死循环
        // 这等同于 visited[r][c] = true;
        grid[r][c] = 0;

        // 3. 【递归计算】
        // 当前面积 = 1 (自己) + 四个方向邻居的面积
        int area = 1; 
        
        // 方向数组定义在函数内，或者做成类的成员变量
        int dr[] = {-1, 1, 0, 0};
        int dc[] = {0, 0, -1, 1};

        for (int i = 0; i < 4; ++i) {
            int nr = r + dr[i];
            int nc = c + dc[i];
            // 直接递归！不需要在 for 循环里写 if 判断越界
            // 因为下一层 dfs 进来第一件事就是检查越界，这样逻辑最解耦。
            area += dfs(grid, nr, nc);
        }

        return area;
    }
};

```
