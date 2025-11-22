**CSMA/CD协议 (Carrier Sense Multiple Access with Collision Detection)**，即 **载波侦听多路访问/冲突检测**。

总线/介质，只允许一个信号通过。
如果俩个信号撞上了，那就混乱了！
那我们让信号一遍传输一遍监听，如果发现真的要撞，就撤回！
待会重试。
这个重试，就是
”二进制指数退避“。
