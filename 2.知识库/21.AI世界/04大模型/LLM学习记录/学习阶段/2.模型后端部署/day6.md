asyncio.sleep 前面要加await ，或者说当有异步函数要执行时，前面await才能把它引出来

浏览器禁止跨域请求，比如前端在3000 后端在8000
app.add_middleware(）  origins（谁能来访问）/credentials（cookie政策）/methods（post、get等方法）/headers 

# openai_api

class一个类 继承basemodel， 填写”变量名：字符类型“，如user_id: str  如果想有默认值直接填就行了
更高级一点，就是optional（选填）、literal（多选1）  如  
- user_name : optional[str]   
- role: Literal["user", "assistant", "system"】
      - **`Optional[Literal["stop", "length"]] = None`**：
    
    - 默认值是 `None`（Python 的空值）。
        
    - 如果用户没有提供值，字段的值为 `None`。
        
     - **`Literal["stop", "length", 'None']`**：

     
        - 没有默认值。
        
        - 如果用户没有提供值，会抛出 `ValidationError`。

- **`Union`**：
    
    - 表示一个变量可以是多种类型中的任意一种。
        
    - 例如：`Union[int, str]` 表示变量可以是 `int` 或 `str`。
        
- **`Literal`**：
    
    - 表示一个变量的值必须是几个固定的值之一。
        
    - 例如：`Literal["stop", "length"]` 表示变量的值只能是 `"stop"` 或 `"length"`

## class
**modelcard** ： 
  有id、object、created（什么时候创建的）、owner、，可选：root、parent、permission
ModelList: 
object、data（modelcard），把modelcard以列表形式展现

ChatMessage：
角色role，对话内容content
DeltaMessage:
角色（可选）、内容（可选）


- `data: {"model":"gpt-3.5-turbo","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"role":"assistant"},"finish_reason":null}]} 
- ``data: {"model":"gpt-3.5-turbo","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"Python"},"finish_reason":null}]}``
可见流式角色和内容都不是一定的，所以是可选


<u>ChatCompletionRequest</u>：<font color="#f79646">请求体</font>
model，message(即刚创建的chatmessage，是list格式，也就是一堆堆message)，temperature，topp，maxlen，stream（是否流式）

<u>ChatCompletionResponseChoice:</u> <font color="#f79646">创建choicedata</font>
index,message(仍然是创建的chatmessage)，finishreason
<u>ChatCompletionResponseStreamChoice:</u>
index, deltamessage, finishreason

<u>CharCompletionResponse:</u>
model,object,choices(选择上方的ChatCompletionResponseChoice或ChatCompletionResponseStreamChoice）


## @app
.get:
服务器自己创建modelcard、最终展示modelist
.post
1. 确保最后一条消息来自用户，否则400错误码
2. 如果请求体的message第一句其实是系统提示词（比如，你是一个好帮手），那把系统提示词提取出来（用pop），然后接下来每一个<font color="#f79646">query</font>都要加上它
3. 初始化<font color="#f79646">history</font> = 【】确保历史消息是严格的user/assistant交替

4. <font color="#f79646">若为流式响应</font>：
   
```python
if request.stream: 
	generate = predict(query, history, request.model) 
	return EventSourceResponse(generate, media_type="text/event-stream")
```
<font color="#f79646"> 若为普通响应</font>：
      ``response,_ = model.chat(tokenizer,query,histtory=history)`
      choicedata，从    choice_data = ChatCompletionResponseChoice(来
      返回ChatCompletionResponse
  
总结：如果请求体的stream是true，那就返回eventsourceresponse，此处有predict函数（携带之前的query、history和请求体里的model）
若不是stream，就用chatcompletionresponsechoice得到chiocedata，携带的messege里，content是model.chat返回出来的，最后的返回是chatcompletionresponse，chioce即为刚才的chiocedata

## predict函数（处理流式）
choice_data = ChatCompletionResponseStreamChoice
chunk等于chatcompletionresponse，如果是普通响应，这里就返回了
加了个yield "{}".format(chunk.json(exclude_unset=True, ensure_ascii=False)) 准备一个词一个词返回


从第一部分代码到最后的predict函数，这些东西实现的，是已有本地model和tokenizer，建立本地服务器，实现get：展示模型，post：客户端发送内容（post方法，必须与定义的请求体格式一样），我们本地def的函数处理内容 并返回openai格式的json数据（model，object，chioce（chioce里是index，chatmessage（rule和content），finishreason）），


## 区别
这个代码可不可以命名为websocket部署chtgpt？实际上，它是接受用户的post，然后把数据转换成url网址的模型。所需要的json模型，以这个网址（如openai）返回的东西作为response，与本地最大的区别就在这。本地的response直接就是model.chat即可


# websocket
## websocketapi
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from fastapi.responses import HTMLResponse

from fastapi.middleware.cors import CORSMiddleware
```
1. 首先在app.add_middleware里，加上CORSMiddleware
2. 将文件夹中的html文件read成html
    只要get根目录，就return HTMLResponse

3. @app.websocket("/ws")  监听路由ws。如果 `@app.get（） 就是http协议，` 接下来
	1. await websocket.accept() 让服务器同意连接
	2. while true开始，首先websocket.receive_json记录下来，收集客户端发的json数据，提取query和history，
	3. 开始流式调用
	
```python
for response, history in model.stream_chat(tokenizer, query, history=history):
streamchat是chatglm独有的，
                await websocket.send_json({

                    "response": response,

                    "history": history,

                    "status": 202,

                })把模型生成的数据，以上述json格式发送出去。202是accepted

            await websocket.send_json({"status": 200})  ok
                    
```

## websocket.html
### 前置工作
首先创建表单form，action=‘’，里面包含input、button
接着创建websocket `let ws = new WebSocket("ws://" + location.host + "/ws");`
和history【】
创建messagebox，公告板区域，（通过ul标签）
### 关键的两个函数
appendmessage：
  不断将聊天对话加入到之前创建的messagebox里，格式是sender：text
sendmessage：
   检查机器人是否正在回复、输入是否为空，其中用户输入由document.getElementById实现