![](../../assets/image/postgreSQL-1775989137291.jpeg)
kkdatabase
![](../../assets/image/postgreSQL-1775989160114.jpeg)

![](../../assets/image/postgreSQL-1775989537842.jpeg)

![](../../assets/image/postgreSQL-1775989614101.jpeg)

![](../../assets/image/postgreSQL-1775989673220.jpeg)



### 1. 左侧树状菜单（资源管理器）：你的“数据集目录”

这是整个数据库的结构树。

- **Databases (2)：** 这里显示你所有的数据库。你已经创建了 AI_Project_DB_KangKai。
    
- **Schemas（模式）：** 点击你的数据库左侧的小箭头，展开后找到 Schemas。再展开 Schemas，你会看到一个 **public**。
    
    - **核心知识：** 在 PostgreSQL 中，表（Tables）不是直接放在数据库下的，而是放在“模式（Schema）”下的。**默认都在 public -> Tables 里**。等会儿我们建完表，就在这里找。
        
- **Extensions（扩展）：** 这个就是以后放 **pgvector**（向量检索插件）的地方。
    

### 2. 中间上部（查询编辑器）：你的“代码实验室”

就是你输入 SELECT version (); 的那个地方。

- 这里是你写 SQL 指令的地方。
    
- **蓝色播放键（或 F5）：** 执行你选中的 SQL 代码。
    
- **软盘图标：** 保存你的 SQL 脚本（可以保存为 . sql 文件，以后重复使用）。
    

### 3. 中间下部（结果面板）：你的“实验报告区”

- **Data Output：** 显示查询出来的表格数据。你刚才看到的 postgres 和数据库名就在这。
    
- **Messages：** 如果你执行代码报错了，或者成功创建了表，这里会提示“Query returned successfully”或者具体的错误代码（比如你刚才遇到的路径非空错误，在这里也会有提示）。
    

### 4. 顶部状态栏：你的“仪表盘”

你会看到一些像心电图一样的波动（Dashboard）。

- **AI 关联点：** 当你以后用 Python 写循环往数据库里塞几百万条 Embedding 向量时，看这里的 CPU 和 Transactions（事务）波动，能帮你判断数据库是否遇到了性能瓶颈。