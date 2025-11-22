mcp是一种协议，如同http协议一样
是一种规范，本来大模型调用外部资源，有好多好多种方法，好多格式，A用A格式，B用B格式，这样会互相不兼容的
mcp就是把格式统一起来
分为mcp client和mcp sever
mcp client 就是大模型，应用端，可以发送请求给mcp sever
mcp sever就是中间人，它收到应用端的请求，开始整合资源， 可以用本地文件，可以用互联网资源




![[mcp技术概述-1752216454486.jpeg]]

mcp的核心代码我们可以人工使用 人工传递参数或者发送请求什么的 但有了mcp协议 就能让大模型自己判断要不要向某个有mcp协议的函数发送请求并使用它
# mcp的使用
上线到model scope平台 平台会替你部署管理
通过SSE URL连接服务
```json
{
  "mcpServers": {
    "12306-mcp": {
      "type": "sse",
      "url": "https://mcp.api-inference.modelscope.net/c5040cde0dc547/sse"
    }
  }
}
```
