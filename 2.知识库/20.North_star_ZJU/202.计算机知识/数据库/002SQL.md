SQL 是结构化查询语言，全称是 Structured Query Language，它是集 **数据查询、数据定义、数据操纵、数据控制** 于一体的关系数据库语言


SQL 的核心特点不用死背，理解这几个即可：

| 特点      | 白话理解                                                                    |
| ------- | ----------------------------------------------------------------------- |
| 综合统一    | 一个 SQL 语言包办查询、建表、改表、删表、授权等操作                                            |
| 高度非过程化  | 你只说“我要什么”，不用告诉数据库“怎么找”                                                  |
| 面向集合    | 一条 SQL 可以查出、删除、更新很多行，不是一行一行处理                                           |
| 可交互也可嵌入 | 可以直接在数据库里执行，也可以嵌入 C、Java 等程序                                            |
| 简洁      | 核心动词少，常见的是 SELECT、CREATE、DROP、ALTER、INSERT、DELETE、UPDATE、GRANT、REVOKE 3 |

这部分大概率出选择题或简答题，不会太难。


### 2. SQL 功能分类：必须会分

SQL 常见功能和动词如下：

|功能|关键词|
|---|---|
|数据查询 DQ| `SELECT` |
|数据定义 DDL| `CREATE`、`DROP`、`ALTER` |
|数据操纵 DML| `INSERT`、`DELETE`、`UPDATE` |
|数据控制 DCL| `GRANT`、`REVOKE` |

考试里如果问“删除表”和“删除数据”的区别，要注意：



```sql
DROP TABLE Student;
```


这是删除整张表，属于 DDL。



```sql
DELETE FROM Student WHERE Sdept = 'CS';
```

这是删除表中的部分行，属于 DML。

### 3. 基本表、视图、存储文件：知道区别

SQL 可以对 **基本表** 和 **视图** 进行查询或其他操作，基本表和视图在概念上都可以看成关系。1

重点区别：

| 对象   | 白话解释                                 |
| ---- | ------------------------------------ |
| 基本表  | 真正独立存在、存数据的表                         |
| 视图   | 从一个或多个基本表导出的“虚表”，数据库中只保存视图定义，不保存视图数据 |
| 存储文件 | 底层真正存放数据的文件，用户一般看不到                  |

视图是虚表，数据实际还在基本表中；用户可以像查询基本表一样查询视图

### 4. SELECT 查询语法：SQL 章的核心

基本格式必须熟：



```sql

SELECT [ALL | DISTINCT] 目标列表达式

FROM 表名或视图名

WHERE 条件表达式

GROUP BY 分组列名

HAVING 分组条件

ORDER BY 排序列名 ASC | DESC;
```


其中 `SELECT` 指定显示哪些列，`FROM` 指定从哪些表或视图查，`WHERE` 指定筛选条件，`GROUP BY` 分组，`HAVING` 筛选分组，`ORDER BY` 排序。7



SELECT 查什么

FROM 从哪查

WHERE 行条件

GROUP BY 怎么分组

HAVING 组条件

ORDER BY 怎么排序

---

### 5. WHERE 条件：选择题和应用题都常考

`WHERE` 常见条件要会写：

| 类型   | 写法                                              |
| ---- | ----------------------------------------------- |
| 比较   | `=`, `<`, `>`, `<=`, `>=`, `<>`                 |
| 范围   | `BETWEEN ... AND ...`，`NOT BETWEEN ... AND ...` |
| 集合   | `IN`，`NOT IN`                                   |
| 字符匹配 | `LIKE`，`NOT LIKE`                               |
| 空值   | `IS NULL`，`IS NOT NULL`                         |
| 复合条件 | `AND`，`OR`，`NOT`                                |


特别注意：判断空值不能写 `= NULL`，必须写：



WHERE Cpno IS NULL

不能写：


WHERE Cpno = NULL

### 6. 单表查询：一定要熟练

常见题型：

#### 查询指定列


```sql

SELECT Sno, Sname

FROM Student;

```

#### 去重查询



```sql
SELECT DISTINCT Sdept

FROM Student;
```


#### 条件查询


```sql
SELECT Sno, Sname

FROM Student

WHERE Sdept = 'CS';

```

#### 范围查询


```sql

SELECT Sno, Sname, Sage

FROM Student

WHERE Sage BETWEEN 18 AND 20;
```


#### 集合查询



```sql
SELECT Sno, Sname

FROM Student

WHERE Sdept IN ('CS', 'IS');
```


#### 模糊查询




```sql
SELECT Sno, Sname

FROM Student

WHERE Sname LIKE '王%';
```


#### 空值查询


```Sql

SELECT Cno, Cname

FROM Course

WHERE Cpno IS NULL;
```



### 7. 连接查询：本章最核心，必须会

课件明确说：连接查询是同时涉及至少两个表的查询，它以广义笛卡尔积为基础，再按照连接条件筛选行，最后投影出需要的列。4  
白话说：**多表查询 = 先拼表，再按条件配对，再选列。**

常见连接条件是两列值相等，也就是等值连接；如果去掉重复属性列，可以看作自然连接。

#### 三表经典模式

数据库考试最常见三个表：


Student (Sno, Sname, Ssex, Sage, Sdept)

Course (Cno, Cname, Cpno, Ccredit)

SC (Sno, Cno, Grade)

你要形成条件反射：

|要查什么|通常涉及表|
|---|---|
|学生基本信息|Student|
|课程基本信息|Course|
|成绩、选课|SC|
|学生选了什么课|Student + SC + Course|
|某学生成绩|Student + SC|
|某课程被谁选|Course + SC + Student|

#### 连接查询模板


```Sql

SELECT 要显示的列

FROM 表 1, 表 2

WHERE 表 1. 公共列 = 表 2. 公共列

  AND 其他条件;
```



---

### 8. 等值连接：最常考

例：查询每个学生及其选课成绩。


```Sql

SELECT Student. Sno, Sname, Cno, Grade

FROM Student, SC

WHERE Student. Sno = SC. Sno;
```

---

### 9. 三表连接：应用题高频

例：查询学生姓名、课程名和成绩。


```Sql

SELECT Sname, Cname, Grade

FROM Student, SC, Course

WHERE Student. Sno = SC. Sno

  AND SC. Cno = Course. Cno;
```


思路：

Text

Student 通过 Sno 连 SC

SC 通过 Cno 连 Course

这是 SQL 应用题最重要的套路。

---

### 10. 自身连接：会看懂即可

自身连接就是一张表和自己连接，必须给表起别名。

例：课程表 `Course(Cno, Cname, Cpno, Ccredit)` 中，`Cpno` 表示先修课号。查询每门课及其先修课名称。


```Sql

SELECT C1. Cname AS 课程名, C2. Cname AS 先修课名

FROM Course C1, Course C2

WHERE C1. Cpno = C2. Cno;

```

白话理解：

- `C1` 当作“当前课程表”
- `C2` 当作“先修课程表”
- `C1.Cpno = C2.Cno` 表示当前课程的先修课号等于另一门课的课程号

---

### 11. 嵌套查询：掌握基础，难的先放

嵌套查询是查询条件中包含子查询的查询，常见形式有 `IN`、比较运算符、`ANY/ALL`、`EXISTS` 等。4  
但根据老师考纲，“比较难的嵌套查询可以不管”，所以重点掌握 `IN` 子查询即可。

#### `IN` 子查询模板


```Sql

SELECT ...

FROM 表

WHERE 某列 IN (

    SELECT 某列

    FROM 表

    WHERE 条件

);

```

例：查询选修了 1 号课程的学生姓名。


```Sql

SELECT Sname

FROM Student

WHERE Sno IN (

    SELECT Sno

    FROM SC

    WHERE Cno = '1'

);

```

这个也可以写成连接查询：


```Sql

SELECT Sname

FROM Student, SC

WHERE Student. Sno = SC. Sno

  AND Cno = '1';
```


考试更推荐你用连接，因为老师强调连接是核心


### 12. 集合查询：知道三个词即可

集合查询使用集合操作把多个查询结果合并，主要有：10

|操作|含义|
|---|---|
| `UNION` |并|
| `INTERSECT` |交|
| `EXCEPT` |差|

这部分如果老师没强调，优先级低于连接查询、单表查询、更新和视图。

---

### 13. 分组查询：注意 WHERE 和 HAVING 区别

#### 聚合函数常见写法

Sql

COUNT (*)      -- 统计行数

COUNT (列名)   -- 统计该列非空值个数

AVG (列名)     -- 平均值

MAX (列名)     -- 最大值

MIN (列名)     -- 最小值

SUM (列名)     -- 求和

课件提醒：集函数不能直接出现在 `WHERE` 子句中，不能复合使用；有分组时，`SELECT` 子句只能出现分组属性或集函数。10

#### 查询每个学生的平均成绩

Sql

SELECT Sno, AVG (Grade) AS AvgGrade

FROM SC

GROUP BY Sno;

#### 查询平均成绩大于 80 的学生

Sql

SELECT Sno, AVG (Grade) AS AvgGrade

FROM SC

GROUP BY Sno

HAVING AVG (Grade) > 80;

关键区别：

|子句|作用|
|---|---|
| `WHERE` |分组前筛选行|
| `HAVING` |分组后筛选组|

---

### 14. ORDER BY：排序

Sql

SELECT Sno, Grade

FROM SC

WHERE Cno = '1'

ORDER BY Grade DESC;

`ASC` 是升序，`DESC` 是降序。`ORDER BY` 一般只用于最外层查询。10

---

### 15. 数据更新：插入、修改、删除

课件总结数据更新包括 `INSERT`、`UPDATE`、`DELETE`，并且一次只能对一张表进行更新；如果需要用到其他表的数据，可以使用子查询。10

#### 插入

Sql

INSERT INTO Student (Sno, Sname, Ssex, Sage, Sdept)

VALUES ('2024001', '张三', '男', 20, 'CS');

#### 修改

Sql

UPDATE Student

SET Sage = Sage + 1

WHERE Sdept = 'CS';

#### 删除

Sql

DELETE FROM Student

WHERE Sdept = 'CS';

注意：

Sql

DELETE FROM Student;

这会删除 `Student` 表中所有元组，但表结构还在。

Sql

DROP TABLE Student;

这会删除整张表，包括表结构。

---

### 16. 视图：语法一定要掌握

视图是从基本表或视图导出的表，属于外模式；它是虚表，数据库只保存定义，不保存视图对应的数据。110

#### 创建视图

Sql

CREATE VIEW 视图名

AS

SELECT ...

FROM ...

WHERE ...;

例如，定义信息系学生视图：

Sql

CREATE VIEW IS_Student

AS

SELECT Sno, Sname, Sage

FROM Student

WHERE Sdept = 'IS';

课件里也给出了这个视图定义例子。9

#### 查询视图

查询视图和查询基本表语法一样。10

Sql

SELECT Sno, Sage

FROM IS_Student

WHERE Sage < 20;

课件例子就是在信息系学生视图中找年龄小于 20 岁的学生学号和年龄。9

#### 删除视图

Sql

DROP VIEW IS_Student;

注意：删除视图只是删除视图定义，不是删除基本表数据。


## 二、典型考试题：直接按这个练

下面按“最可能考”的顺序来。

---

### 题 1：写出 SQL 查询语句的基本格式，并说明各子句作用。

答案：

Sql

SELECT [ALL | DISTINCT] 目标列表达式

FROM 表名或视图名

WHERE 条件表达式

GROUP BY 分组列名

HAVING 分组条件

ORDER BY 排序列名 ASC | DESC;

解释：

- `SELECT`：指定要显示的列；
- `FROM`：指定查询对象，可以是基本表或视图；
- `WHERE`：筛选满足条件的行；
- `GROUP BY`：按照某列分组；
- `HAVING`：筛选满足条件的组；
- `ORDER BY`：排序。7

---

### 题 2：查询所有计算机系学生的学号和姓名。

假设计算机系代码是 `'CS'`：

Sql

SELECT Sno, Sname

FROM Student

WHERE Sdept = 'CS';

公式：

Sql

SELECT 要查的列

FROM 表

WHERE 条件;

---

### 题 3：查询年龄在 18 到 20 岁之间的学生。

Sql

SELECT Sno, Sname, Sage

FROM Student

WHERE Sage BETWEEN 18 AND 20;

`BETWEEN ... AND ...` 用于范围查询。4

---

### 题 4：查询没有先修课的课程。

课程表一般是：

Text

Course (Cno, Cname, Cpno, Ccredit)

其中 `Cpno` 是先修课号，空值表示没有先修课。

Sql

SELECT Cno, Cname

FROM Course

WHERE Cpno IS NULL;

注意：空值判断必须用 `IS NULL`。4

---

### 题 5：查询姓“王”的学生。

Sql

SELECT Sno, Sname

FROM Student

WHERE Sname LIKE '王%';

`LIKE` 用于字符匹配。4

---

### 题 6：查询选修了 1 号课程的学生学号和成绩。

Sql

SELECT Sno, Grade

FROM SC

WHERE Cno = '1';

---

### 题 7：查询选修了 1 号课程的学生姓名和成绩。

涉及两个表：`Student` 和 `SC`。

Sql

SELECT Sname, Grade

FROM Student, SC

WHERE Student. Sno = SC. Sno

  AND SC. Cno = '1';

解题公式：

Text

学生姓名在 Student

成绩在 SC

两表通过 Sno 连接

所以：

Sql

FROM Student, SC

WHERE Student. Sno = SC. Sno

---

### 题 8：查询每个学生的姓名、课程名和成绩。

涉及三张表：

- 学生姓名：`Student`
- 课程名：`Course`
- 成绩：`SC`

Sql

SELECT Sname, Cname, Grade

FROM Student, SC, Course

WHERE Student. Sno = SC. Sno

  AND SC. Cno = Course. Cno;

连接查询是多表查询的核心，它以笛卡尔积为基础，再用连接条件筛选出需要的行。4

---

### 题 9：查询选修“数据库”课程的学生姓名和成绩。

Sql

SELECT Sname, Grade

FROM Student, SC, Course

WHERE Student. Sno = SC. Sno

  AND SC. Cno = Course. Cno

  AND Course. Cname = '数据库';

解题口诀：

Text

看到学生姓名 -> Student

看到课程名 -> Course

看到成绩 -> SC

三表连接：Student. Sno = SC. Sno，SC. Cno = Course. Cno

---

### 题 10：查询每个学生的平均成绩。

Sql

SELECT Sno, AVG (Grade) AS AvgGrade

FROM SC

GROUP BY Sno;

---

### 题 11：查询平均成绩大于 80 分的学生学号。

Sql

SELECT Sno

FROM SC

GROUP BY Sno

HAVING AVG (Grade) > 80;

注意：聚合函数条件放 `HAVING`，不要放 `WHERE`。10

错误写法：

Sql

SELECT Sno

FROM SC

WHERE AVG (Grade) > 80

GROUP BY Sno;

---

### 题 12：查询选课人数超过 3 人的课程号。

Sql

SELECT Cno

FROM SC

GROUP BY Cno

HAVING COUNT (*) > 3;

---

### 题 13：将所有计算机系学生年龄加 1。

Sql

UPDATE Student

SET Sage = Sage + 1

WHERE Sdept = 'CS';

更新操作用 `UPDATE`。10

---

### 题 14：删除没有成绩的选课记录。

Sql

DELETE FROM SC

WHERE Grade IS NULL;

删除操作用 `DELETE`，空值判断用 `IS NULL`。410

---

### 题 15：删除选修 1 号课程的所有选课记录。

Sql

DELETE FROM SC

WHERE Cno = '1';

注意这是删除 `SC` 表中的记录，不是删除课程表里的课程。

---

### 题 16：建立信息系学生视图。

Sql

CREATE VIEW IS_Student

AS

SELECT Sno, Sname, Sage

FROM Student

WHERE Sdept = 'IS';

视图是从基本表导出的虚表，数据库只保存视图定义，不保存实际数据。1

---

### 题 17：在信息系学生视图中查询年龄小于 20 岁的学生学号和年龄。

Sql

SELECT Sno, Sage

FROM IS_Student

WHERE Sage < 20;

课件里给的例子就是在 `IS_Student` 视图中查询年龄小于 20 的学生学号和年龄。9

---

### 题 18：删除信息系学生视图。

Sql

DROP VIEW IS_Student;

注意：`DROP VIEW` 删除的是视图定义，不删除 `Student` 表中的学生数据。

---

### 题 19：查询每门课程及其先修课名称。

课程表：

Text

Course (Cno, Cname, Cpno, Ccredit)

自身连接写法：

Sql

SELECT C1. Cname AS 课程名, C2. Cname AS 先修课名

FROM Course C1, Course C2

WHERE C1. Cpno = C2. Cno;

自身连接就是表和自己连接，必须使用别名。4

---

### 题 20：用嵌套查询查询选修了 1 号课程的学生姓名。

Sql

SELECT Sname

FROM Student

WHERE Sno IN (

    SELECT Sno

    FROM SC

    WHERE Cno = '1'

);

嵌套查询就是查询条件中包含子查询，`IN` 是常见子查询形式。4

但如果考试没要求“用嵌套查询”，更推荐写连接：

Sql

SELECT Sname

FROM Student, SC

WHERE Student. Sno = SC. Sno

  AND SC. Cno = '1';

---

## 三、这一章你应该优先背/练的顺序

### 第一优先级：必须会写

1. `SELECT ... FROM ... WHERE ...`
2. `BETWEEN`、`IN`、`LIKE`、`IS NULL`
3. 两表连接、三表连接
4. `GROUP BY ... HAVING ...`
5. `UPDATE`
6. `DELETE`
7. `CREATE VIEW`
8. `DROP VIEW`

---

### 第二优先级：会看懂即可

1. 自身连接
2. `DISTINCT`
3. `ORDER BY`
4. 简单 `IN` 嵌套查询
5. `UNION / INTERSECT / EXCEPT`

---

### 第三优先级：先跳过或少花时间

1. 很复杂的 `EXISTS`
2. `ANY / ALL`
3. 复杂相关子查询
4. 索引细节
5. SQL 发展历史

---

## 四、SQL 应用题万能解题模板

### 1. 先找涉及哪些表

|题目关键词|找哪张表|
|---|---|
|学号、姓名、性别、年龄、系| `Student` |
|课程号、课程名、学分、先修课| `Course` |
|成绩、选课| `SC` |

---

### 2. 再写连接条件

Sql

Student. Sno = SC. Sno

SC. Cno = Course. Cno

---

### 3. 最后写筛选条件

例如：

Sql

AND Course. Cname = '数据库'

AND Grade > 80

AND Sdept = 'CS'

---

### 4. 完整模板

Sql

SELECT 要显示的列

FROM Student, SC, Course

WHERE Student. Sno = SC. Sno

  AND SC. Cno = Course. Cno

  AND 题目给的筛选条件;

这就是 SQL 应用题最常用的套路。