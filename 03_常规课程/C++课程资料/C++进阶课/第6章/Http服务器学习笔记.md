# 第6章：HTTP服务器 —— 完整学习笔记

> **前置章节**：第5章 网络编程
> **预计学习时间**：1.0 小时
> **配套材料**：第六章Http服务器.pdf + http目录源码（main.cpp / http.cpp / custom_handle.cpp / wwwroot资源）

---

## 一、知识点黄金四步法讲解

### 1.1 万维网与URL【了解】

#### 是什么
万维网（World Wide Web，简称 WWW/Web）是一个大规模的、联机式的信息储藏所，通过超链接把分布在世界各地的信息源串联起来，用户可以按需获取信息。URL（Uniform Resource Locator，统一资源定位符）是万维网中资源的唯一标识地址。

**生活比喻**：万维网就像一座全球图书馆，URL就是每本书的索书号——只要你写出正确的索书号，图书管理员就能帮你精准找到那本书。

#### 为什么
- 第一层：为什么需要万维网？因为信息分散在全球各地，需要一种机制把它们关联起来。
- 第二层：为什么用URL来定位？因为需要一个统一的命名规则，让任何客户端都能按相同格式请求资源。
- 第三层：本质是什么？URL是应用层协议（HTTP）寻址的基础，没有URL就没有Web的请求与响应。

#### 怎么用
URL由四部分组成：`协议://主机名:端口号/路径`

```
http://www.baidu.com.cn:80/index.html
^^^^   ^^^^^^^^^^^^^^^^  ^^  ^^^^^^^^^^^
协议      主机名         端口    路径
```

- **协议**：指出使用何种协议获取文档，常用 `http`（默认端口80）、`https`（默认端口443）。
- **主机名**：文档所在主机的域名或IP地址。
- **端口号**：协议对应的端口，HTTP默认为80，可省略不写。
- **路径**：超文本文档在服务器上的存储路径。

浏览器访问 `http://192.168.1.100:8080/login.html` 时，会向 192.168.1.100 的 8080 端口发起 TCP 连接，然后发送 HTTP GET 请求 `/login.html`。

#### 注意事项
- URL中的端口号如果与协议默认端口一致可以省略，但自定义端口必须显式写出。
- 路径部分区分大小写（Linux服务器上），`/Index.html` 和 `/index.html` 是两个不同的资源。

> **人话总结**：URL就是网络资源的精确地址。

---

### 1.2 HTML基础标签【熟悉】

#### 是什么
HTML（HyperText Markup Language，超文本标记语言）是用来编写超文本文档的语言，它不是协议，而是浏览器能够识别并渲染的排版语言。HTML文件后缀为 `.html` 或 `.htm`。

**生活比喻**：HTML就像一份带格式标记的手稿——作者用"标题""段落""加粗"等标记告诉排版工人如何呈现内容，浏览器就是这个排版工人。

#### 为什么
- 第一层：为什么需要HTML？纯文本无法表达标题、链接、图片等丰富排版，需要一种标准化的描述方式。
- 第二层：为什么用标签而不是二进制格式？标签是人类可读的文本格式，方便编辑和调试。
- 第三层：本质是什么？HTML是HTTP响应体中最常见的内容类型，服务器返回HTML，浏览器解析后呈现界面。

#### 怎么用

**标签分类**：
| 类别 | 格式 | 示例 |
|------|------|------|
| 单标签（空标签） | `<标签名/>` | `<br/>`、`<input/>` |
| 双标签 | `<标签名>内容</标签名>` | `<h1>标题</h1>`、`<p>段落</p>` |

**常用标签速查**：

| 标签 | 作用 | 备注 |
|------|------|------|
| `h1~h6` | 一至六级标题 | h1最大，h6最小 |
| `p` | 段落 | 自动上下留白 |
| `div` | 块级容器（盒子） | 布局核心标签 |
| `input` | 输入框 | type属性决定类型 |
| `a` | 超链接 | href指定目标URL |
| `br` | 换行 | 单标签 |
| `form` | 表单容器 | method指定GET/POST |

**第一个HTML文件**（配套代码 `wwwroot/index.html`）：

```html
<!DOCTYPE html>          <!-- 声明文档类型为HTML5 -->
<html lang="en">         <!-- 根标签，lang指定语言 -->
<head>                   <!-- 头部：元信息，不在页面显示 -->
    <meta charset="UTF-8">   <!-- 编码格式 -->
    <title>Document</title>   <!-- 浏览器标签页标题 -->
</head>
<body>                   <!-- 主体：页面可见内容 -->
    <h1>主页 GET 请求示例</h1>
    <h1>欢迎来到星球部落</h1>
</body>
</html>
```

执行结果：浏览器打开后显示两行一级标题文字，标签页标题显示"Document"。

**VSCode快速创建**：新建 `.html` 文件 → 输入 `html:5` 或 `!` → 按Tab键自动补全模板。安装 Live Server 扩展可实时预览。

#### 注意事项
- `<!DOCTYPE html>` 必须是文件第一行，否则浏览器可能进入怪异模式（Quirks Mode），导致CSS渲染异常。
- `<meta charset="UTF-8">` 必须放在 `<head>` 内靠前位置，否则中文可能乱码。
- 标签必须正确嵌套：`<b><i>文字</i></b>` 是正确的，`<b><i>文字</b></i>` 是错误的。

> **人话总结**：HTML是用标签描述网页排版的语言。

---

### 1.3 HTTP协议特点【重点】

#### 是什么
HTTP（HyperText Transfer Protocol，超文本传输协议）定义了浏览器如何从服务器请求超文本，以及服务器如何将文档传递给浏览器。它是面向事务的应用层协议，底层使用TCP进行可靠传输。

**生活比喻**：HTTP就像去餐厅点菜——你（客户端）看菜单向服务员（服务器）报菜名（发请求），服务员把菜端上来（响应），但你每次来都要重新报菜名，服务员不记得你上次点了什么（无状态），而且说完一句话就挂电话，下次再打要重新拨号（无连接）。

#### 为什么
- 第一层：为什么HTTP是面向事务的？一次完整的交互（建立连接→发送请求→接收响应→断开连接）是不可分割的整体，要么全部完成要么全部不做。
- 第二层：为什么强调可靠？因为网页内容不能丢包或缺损，所以HTTP选择了TCP作为传输层协议。
- 第三层：为什么设计成无状态和无连接？早期网络带宽极其有限，保持连接会浪费服务器资源；无状态使服务器实现简单、易于水平扩展。

#### 怎么用
HTTP的核心特征：

| 特征 | 含义 | 实际影响 |
|------|------|----------|
| 面向事务 | 请求-响应是一个不可分割的整体 | 事务内任一步骤失败则整体失败 |
| 可靠传输 | 基于TCP协议 | 数据不会丢失或乱序 |
| 客户端发起 | 永远是客户端先请求，服务器才能响应 | 服务器无法主动推送（HTTP/1.x） |
| 无状态 | 服务器不记忆客户端的历史请求 | 需要Cookie/Session弥补 |
| 无连接 | 每个连接只处理一个请求后立即断开 | HTTP/1.0的特点，1.1改为长连接 |

**工作流程**：
1. 客户端与服务器建立TCP连接（三次握手）
2. 客户端发送HTTP请求报文
3. 服务器处理请求并返回HTTP响应报文
4. 客户端展示响应内容
5. 断开TCP连接（HTTP/1.0立即断开；HTTP/1.1保持一段时间）

用 `curl -v http://localhost:8080/index.html` 可以观察到完整的请求/响应报文：
```
* Connected to localhost (127.0.0.1) port 8080
> GET /index.html HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.68.0
> Accept: */*
>
< HTTP/1.1 200 OK
< Content-Type: text/html
<
<!DOCTYPE html>...
```

#### 注意事项
- "无状态"不等于"不需要身份验证"。通过Cookie和Session机制可以在无状态协议上实现有状态的会话管理。
- "无连接"在HTTP/1.1中已被长连接（Keep-Alive）取代，但逻辑上仍然是请求-响应模型。
- 错误理解："HTTP不安全"——HTTP本身只是明文传输，安全问题通过HTTPS（TLS加密）解决。

> **人话总结**：HTTP是无状态的请求-响应协议。

---

### 1.4 HTTP版本演进【重点】

#### 是什么
HTTP协议经历了1.0→1.1→2.0→3.0四个主要版本的演进，以及HTTPS安全增强版本。每个版本都在解决上一版本的核心瓶颈。

**生活比喻**：HTTP版本演进就像快递系统的升级——1.0是每次寄信都跑一趟邮局（短连接串行）；1.1是一次去邮局可以连续寄多封信但必须排队取件（长连接+管道化但有队头阻塞）；2.0是把信件拆成编号小包并发运送（stream并发+头部压缩）；3.0是把公路换成高铁，彻底摆脱老路的拥堵（QUIC基于UDP）。

#### 为什么
- 第一层：为什么要不断升级？Web页面越来越复杂，资源越来越多，旧版本的性能瓶颈成为用户体验的障碍。
- 第二层：各版本分别解决了什么问题？1.1解决短连接开销，2.0解决头部冗余和并发限制，3.0解决TCP层面的队头阻塞和握手延迟。
- 第三层：本质是什么？每一代升级都是在"减少等待时间、提高传输效率、增强安全性"三个维度上做优化。

#### 怎么用

**HTTP版本对比表**：

| 特性 | HTTP/1.0 | HTTP/1.1 | HTTP/2.0 | HTTP/3.0 |
|------|----------|----------|----------|----------|
| 发布时间 | 1996年 | 1997年 | 2015年 | 2022年(RFC) |
| 连接方式 | 短连接 | 长连接(Keep-Alive) | 长连接+多路复用 | QUIC(基于UDP) |
| 并发能力 | 串行请求 | 管道化(响应仍有序) | stream并发 | stream并发 |
| 头部压缩 | 无 | 无 | HPACK算法 | QPACK算法 |
| 传输编码 | ASCII文本 | ASCII文本 | 二进制帧 | 二进制帧 |
| 服务器推送 | 不支持 | 不支持 | 支持(PUSH_PROMISE) | 支持 |
| 队头阻塞 | 请求级阻塞 | 响应级阻塞 | 应用层无阻塞 | 完全无阻塞 |
| 传输层协议 | TCP | TCP | TCP | UDP(QUIC) |
| 握手次数 | TCP 3次 | TCP 3次 | TCP 3次+TLS | QUIC 1-RTT/0-RTT |
| 网络迁移 | 需重连 | 需重连 | 需重连 | 基于Connection ID无缝迁移 |
| 安全性 | 明文 | 明文(可选TLS) | 通常配TLS | 内置加密 |

**HTTP/1.0的问题**：
- 每个请求都要新建TCP连接，三次握手开销大
- 串行请求，前一个未完成后续不能发送
- 明文传输，容易被窃听

**HTTP/1.1的改进**：
- 长连接：只要任意一端未明确提出断开，TCP连接一直保持
- 管道化：同一连接可发送多个请求，不必等前一个响应
- 不足：响应仍按请求顺序返回（响应队头阻塞）；头部依然巨大且重复；ASCII编码效率低；并发连接数有限（浏览器通常最多6个）

**HTTP/2.0的改进**：
- HPACK头部压缩：合并重复字段，节约带宽
- stream并发：引入stream概念，一个TCP连接上可同时传输多个stream
- 服务器推送：服务器可主动发送PUSH_PROMISE帧预告即将推送的资源
- 二进制分帧：不再使用ASCII文本格式
- 不足：TCP层的队头阻塞仍存在；TCP握手延迟；网络迁移需重连

**HTTP/3.0的改进**：
- 传输层改用UDP上的QUIC协议
- QUIC内置连接管理、拥塞控制、流量控制
- 每个stream独立，丢包只影响该stream，不影响其他stream
- 基于Connection ID而非四元组连接，支持网络无缝迁移
- 握手可与TLS合并，实现1-RTT甚至0-RTT建连

**HTTPS**：
- 在HTTP和TCP之间加入TLS协议层
- 提供信息加密、完整性校验、身份认证
- TLS四次握手发生在TCP三次握手之后
- 增加了约1-2个RTT的连接建立延迟，但确保了信息安全

#### 注意事项
- HTTP/1.1的管道化在实际浏览器中大多默认关闭或不支持，不要假设它一定生效。
- HTTP/2.0虽然解决了应用层的队头阻塞，但TCP层的队头阻塞依然存在，这是推动HTTP/3.0诞生的根本原因。
- HTTPS的TLS握手是耗时操作，但在现代硬件和网络条件下影响已大幅降低。

> **人话总结**：HTTP版本越新越快越安全。

---

### 1.5 HTTP请求报文格式【重点】

#### 是什么
HTTP请求报文是从客户端发送给服务器的数据格式，由三部分组成：请求行（开始行）、首部行、实体主体。

**生活比喻**：请求报文就像一封挂号信——信封上写着收件人和寄件方式（请求行），信纸开头列出了附加说明如"紧急""回执"（首部行），信的正文就是你要传递的内容（实体主体）。

#### 为什么
- 第一层：为什么要有固定格式？服务器需要按照统一规则解析来自不同客户端的请求。
- 第二层：为什么分三部分？请求行说明"做什么"，首部行说明"怎么做"，实体主体携带"做的内容"，职责清晰。
- 第三层：本质是什么？报文格式是HTTP协议的语法规范，是客户端和服务器沟通的"共同语言"。

#### 怎么用

**请求报文结构**：
```
请求行：方法 URL 版本\r\n
首部行：字段名: 值\r\n
       字段名: 值\r\n
       \r\n              ← 空行分隔
实体主体：（GET通常为空，POST携带表单数据）
```

**请求方法详解**：

| 方法 | 作用 | 是否有Body | 是否幂等 | 典型场景 |
|------|------|-----------|---------|---------|
| GET | 请求资源 | 否 | 是 | 浏览网页、搜索 |
| POST | 提交数据 | 是 | 否 | 登录、上传文件 |
| HEAD | 只获取响应头 | 否 | 是 | 检查资源是否存在 |
| PUT | 上传/替换资源 | 是 | 是 | RESTful更新 |
| DELETE | 删除资源 | 否 | 是 | RESTful删除 |
| OPTIONS | 查询支持的方法 | 否 | 是 | CORS预检 |
| TRACE | 环回测试 | 否 | 是 | 诊断代理链路 |
| CONNECT | 建立隧道 | 否 | 否 | HTTPS代理 |

**GET请求实例**：
```
GET /index.html HTTP/1.1\r\n
Host: 192.168.1.100:8080\r\n
User-Agent: Mozilla/5.0\r\n
Accept: text/html\r\n
\r\n
```

**POST请求实例**：
```
POST /login.html HTTP/1.1\r\n
Host: 192.168.1.100:8080\r\n
Content-Type: application/x-www-form-urlencoded\r\n
Content-Length: 35\r\n
\r\n
username=admin&password=123456
```

注意要点：
- 请求行的三部分用空格隔开，末尾是 `\r\n`
- 每个首部行以 `\r\n` 结尾
- 首部行结束后必须有一个空行 `\r\n` 来分隔首部和实体主体
- GET请求的参数附在URL后面（`?key=value&key2=value2`），POST请求的参数放在实体主体中

#### 注意事项
- GET请求的URL长度受浏览器和服务器的限制（通常2048字节左右），不适合传大量数据。
- POST请求必须在首部中包含 `Content-Length`，否则服务器不知道要读取多少字节的Body。
- 请求方法是大小写敏感的，规范要求大写（GET、POST），但有些服务器做了容错处理（如本章源码中使用 `strcasecmp` 做不区分大小写比较）。

> **人话总结**：请求报文=方法+地址+版本+头部+正文。

---

### 1.6 HTTP响应报文格式【重点】

#### 是什么
HTTP响应报文是服务器返回给客户端的数据格式，同样由三部分组成：状态行（开始行）、首部行、实体主体。

**生活比喻**：响应报文就像快递的回执单——上面写着"已签收/拒收/地址有误"（状态码），附带一些补充说明（首部行），包裹本身就是你要的文件内容（实体主体）。

#### 为什么
- 第一层：为什么需要状态码？客户端需要根据不同的处理结果做出不同反应（成功显示页面、失败提示用户、重定向跳转）。
- 第二层：为什么分五类？1xx信息、2xx成功、3xx重定向、4xx客户端错误、5xx服务器错误，覆盖了所有可能的交互结果。
- 第三层：本质是什么？状态码是服务器对请求的标准化应答语义，让客户端能程序化处理各种情况。

#### 怎么用

**响应报文结构**：
```
状态行：版本 状态码 短语\r\n
首部行：字段名: 值\r\n
       \r\n              ← 空行分隔
实体主体：HTML文件内容/JSON数据等
```

**五类状态码详解**：

| 类别 | 含义 | 常见状态码 | 说明 |
|------|------|-----------|------|
| 1xx | 信息 | 100 Continue | 请求已接收，继续处理 |
| 2xx | 成功 | 200 OK | 请求成功，正常返回内容 |
| 3xx | 重定向 | 301 Moved Permanently | 资源永久移动到新URL |
| 3xx | 重定向 | 304 Not Modified | 资源未修改，可用缓存 |
| 4xx | 客户端错误 | 400 Bad Request | 请求语法错误 |
| 4xx | 客户端错误 | 401 Unauthorized | 认证失败 |
| 4xx | 客户端错误 | 403 Forbidden | 服务器拒绝提供服务 |
| 4xx | 客户端错误 | 404 Not Found | 请求的资源不存在 |
| 5xx | 服务器错误 | 500 Internal Server Error | 服务器内部不可预测的错误 |
| 5xx | 服务器错误 | 503 Service Unavailable | 服务器暂时无法处理请求 |

**响应报文实例**（本章服务器返回200时）：
```
HTTP/1.1 200 OK\r\n
\r\n
<!DOCTYPE html><html>...</html>
```

**404响应实例**（本章 `show_404` 函数构造）：
```
HTTP/1.1 404 Not Found\r\n
\r\n
<!DOCTYPE html><html><body><h1>404 Not Found</h1></body></html>
```

#### 注意事项
- 状态行中版本、状态码、短语三者之间用空格隔开，缺一不可。
- 304 Not Modified 不返回实体主体，仅通知客户端使用本地缓存。
- 400和404的区别：400是请求格式有问题（服务器无法解析），404是请求格式正确但资源不存在。
- 500和503的区别：500是服务器内部出了bug，503是服务器过载或维护中，稍后可能恢复。

> **人话总结**：状态码是服务器回复的数字暗号。

---

### 1.7 HTTP服务器原理【重点】

#### 是什么
HTTP服务器本质上是一个TCP服务器，在accept到客户端连接后，解析HTTP请求报文，根据URL查找对应文件，构造HTTP响应报文并通过socket发送回客户端。

**生活比喻**：HTTP服务器就像一个自助餐厅的服务窗口——你递进去一张点菜单（HTTP请求），窗口里的人看菜单找到对应的菜品（文件），装盘贴上标签（构造响应报文）递出来给你。

#### 为什么
- 第一层：为什么不直接用TCP收发原始数据？因为浏览器只认HTTP格式的报文，裸TCP数据浏览器无法解析。
- 第二层：为什么用多线程处理并发？每个客户端请求的处理时间不确定，如果串行处理会导致后续客户端长时间等待。
- 第三层：本质是什么？HTTP服务器 = TCP通信基础设施 + HTTP协议解析 + 文件系统映射 + 业务逻辑扩展。

#### 怎么用

**架构划分**（本章源码的三层架构）：

```
┌──────────────┐     ┌──────────────┐     ┌─────────────────┐
│  main.cpp    │────→│  http.cpp    │────→│ custom_handle   │
│  主循环+accept│     │ TCP初始化    │     │ .cpp            │
│  线程创建     │     │ 请求解析     │     │ 自定义业务逻辑   │
│              │     │ 响应构造     │     │ (求和/登录)      │
└──────────────┘     └──────────────┘     └─────────────────┘
```

- **main.cpp**：负责创建服务器、accept循环、为每个连接创建独立线程。
- **http.cpp**：负责TCP初始化（socket/bind/listen）、HTTP请求解析（提取方法/URL/参数）、分发到对应处理函数、构造标准HTTP响应。
- **custom_handle.cpp**：负责具体业务逻辑（求和计算、登录验证），与HTTP协议细节解耦。

**完整数据流**（一个GET请求从进入到响应的全过程）：
1. `main()` 中 `accept()` 获得通信fd
2. `pthread_create` 创建线程，将fd传给 `msg_request()`
3. `msg_request()` 调用 `handler_msg(sock)`
4. `handler_msg()` 用 `MSG_PEEK` 预览数据，再用 `get_line()` 读取请求行
5. 解析出method和url，拼接路径 `../wwwroot + url`
6. 用 `stat()` 检查文件是否存在
7. 若存在且是纯GET：调用 `echo_www()` → send状态行 + 空行 + sendfile发送文件
8. 若不存在：调用 `echo_error(404)` → `show_404()` 发送404页面
9. 若是POST或带参数的GET：调用 `handle_request()` → 解析Body → 调用 `parse_and_process()`
10. 处理完毕后 `close(sock)` 关闭连接

#### 注意事项
- 服务器的工作目录决定了相对路径的基准，本章使用 `../wwwroot` 是因为编译产物在 `build/` 子目录下。
- `sendfile()` 是零拷贝系统调用，比 read+write 效率高，但只能用于文件到socket的传输。
- 生产级HTTP服务器还需要处理超时、限流、日志、MIME类型映射等，本章是教学简化版。

> **人话总结**：HTTP服务器=TCP+协议解析+文件服务。

---

## 二、配套代码逐行走读

### 2.1 CMakeLists.txt 构建配置

```cmake
# 规定CMake最小版本为2.8
cmake_minimum_required(VERSION 2.8)

# 项目名称为thttpd（tiny http daemon的缩写）
project(thttpd)

# 将三个源文件编译为可执行文件thttpd.out
add_executable(thttpd.out main.cpp http.cpp custom_handle.cpp)

# 链接pthread线程库，因为代码使用了pthread_create等POSIX线程API
target_link_libraries(thttpd.out pthread)
```

**走读要点**：
- `thttpd` 命名遵循Unix传统（t表示tiny/teaching），表明这是一个教学用的微型HTTP服务器。
- 必须链接 `pthread` 库，否则 `pthread_create`、`pthread_detach` 等函数在链接阶段会报 undefined reference 错误。
- 编译命令等价于：`g++ main.cpp http.cpp custom_handle.cpp -o thttpd.out -lpthread`

---

### 2.2 http.h 头文件

```c
#ifndef HTTP_H           // 头文件守卫，防止重复包含
#define HTTP_H

#define SIZE 4096        // 定义接收缓冲区大小为4096字节

// 声明初始化服务器函数：传入端口号，返回监听套接字fd
int init_server(int _port);

// 声明消息处理函数：传入客户端通信套接字fd，处理完整的HTTP请求-响应流程
int handler_msg(int sock);

#endif
```

**走读要点**：
- `SIZE 4096` 是整个项目中recv缓冲区和字符串容器的统一大小，4KB是Linux内存页大小，对齐有利于性能。
- 头文件中只有声明没有定义，符合C/C++分离编译原则。

---

### 2.3 custom_handle.h 头文件

```c
#ifndef CUSTOM_HANDLE_H
#define CUSTOM_HANDLE_H

// 声明业务处理入口函数
// 参数：sock=客户端fd, querry_string=URL中?后的查询串, req_buf=POST Body数据
int parse_and_process(int sock, const char *querry_string, char *req_buf);

#endif
```

**走读要点**：
- `parse_and_process` 是业务逻辑的统一入口，http.cpp 只负责协议层面，不涉及具体业务。
- 这种分层设计使得新增业务（如注册接口）只需修改 custom_handle.cpp，无需改动协议解析代码。

---

### 2.4 main.cpp 主程序逐行走读

```cpp
#include <myhead.h>      // 自定义公共头文件，包含stdio/stdlib/string/pthread/sys/socket等
#include "http.h"        // 包含init_server和handler_msg的声明

// ========== 线程体函数：每个客户端连接由一个独立线程执行此函数 ==========
void *msg_request(void *arg)
{
    // arg是new int(sock)传来的堆上指针，解引用获取实际的socket fd
    int sock = *(int *)arg;
    // 释放堆上分配的int内存，防止内存泄漏
    delete (int *)arg;
    // 调用HTTP请求处理函数，这是整个请求处理的核心入口
    handler_msg(sock);
    // 处理完毕后关闭通信套接字，释放内核资源
    close(sock);
    // 线程函数返回NULL，pthread_create要求返回void*
    return NULL;
}

// ========== 主函数 ==========
int main(int argc, const char *argv[])
{
    int port = 80;       // 默认使用HTTP标准端口80

    // 如果命令行传了参数，用atoi将字符串转为整数作为端口号
    if (argc > 1)
    {
        port = atoi(argv[1]);
        // atoi("8080") → 8080; atoi("abc") → 0（不会报错，需注意）
    }

    // 调用自定义初始化函数，完成socket→bind→listen全流程
    // 返回值lis_socket是监听套接字，专门用于accept新连接
    int lis_socket = init_server(port);

    // 无限循环接收客户端连接
    while (1)
    {
        struct sockaddr_in peer;      // 存储客户端地址信息的结构体
        socklen_t len = sizeof(peer); // accept需要传入地址结构体的长度

        // 阻塞等待客户端连接，返回新的通信fd
        // lis_socket继续监听，sock是与该客户端专用的通信fd
        int sock = accept(lis_socket, (struct sockaddr *)&peer, &len);
        if (sock == -1)               // accept失败（如被信号中断）
        {
            perror("accept error");
            return -1;
        }

        printf("您有新的客户端(%d)发来连接请求了\n", sock);

        // 为新连接创建一个独立线程
        // new int(sock)：在堆上分配一个int存放sock值，作为线程参数传入
        // 之所以用堆分配而非直接传&sock，是因为sock是栈变量，
        // 下一轮循环会覆盖它，线程可能读到错误的值
        pthread_t tid = -1;
        if (pthread_create(&tid, NULL, msg_request, new int(sock)) > 0)
        {
            printf("pthread_create error\n");
            return -1;
        }

        // 将线程设为分离态：线程结束后自动回收资源
        // 不调用detach也不调用join会导致线程资源泄漏（僵尸线程）
        pthread_detach(tid);
    }

    // 理论上不会执行到这里（while(1)无限循环）
    close(lis_socket);
    return 0;
}
```

**关键内存安全分析**：
- `new int(sock)` 配合 `delete (int *)arg` 构成了完整的堆内存生命周期管理。
- 如果误用 `&sock` 传参：主线程的while循环可能在子线程读取之前就修改了sock的值，导致子线程拿到错误的fd，产生难以排查的bug。
- `pthread_detach` 必须在 `pthread_create` 成功后立即调用，否则线程退出后其返回值和资源不会被自动清理。

---

### 2.5 http.cpp 核心协议处理逐行走读

#### 2.5.1 init_server 函数

```cpp
int init_server(int _port)
{
    // 创建TCP套接字：AF_INET=IPv4, SOCK_STREAM=流式(TCP), 0=自动选择协议
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if(sock == -1) { perror("socke error"); return -1; }

    // 设置端口复用选项：允许服务器重启后立即绑定同一端口
    // 不设此项时，服务器关闭后端口处于TIME_WAIT状态，需等60秒才能重用
    int reuse = 1;
    if(setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse))==-1)
    { perror("setsockopt error"); return -1; }

    // 填充服务器地址结构体
    struct sockaddr_in local;
    local.sin_family = AF_INET;           // IPv4协议族
    local.sin_port = htons(_port);        // 端口号转网络字节序（大端）
    local.sin_addr.s_addr = INADDR_ANY;   // 0.0.0.0，接收任意网卡的连接

    // 将套接字与地址绑定
    if(bind(sock, (struct sockaddr*)&local, sizeof(local))==-1)
    { perror("bind error"); return -1; }

    // 启动监听，backlog=128表示等待队列最大长度
    if(listen(sock, 128) == -1)
    { perror("listen error"); return -1; }

    return sock;  // 返回监听套接字
}
```

**走读要点**：
- `SO_REUSEADDR` 是开发调试阶段的必备选项，否则每次修改代码重启服务器都会遇到 "Address already in use" 错误。
- `htons` 将主机字节序（小端x86）转换为网络字节序（大端），跨平台通信必须做此转换。
- `INADDR_ANY` 等价于 `0.0.0.0`，表示监听所有网络接口；若只想监听本机可用 `inet_addr("127.0.0.1")`。
- `listen` 的 backlog 参数 128 是全连接队列上限，超过此数量的新连接会被内核拒绝。

#### 2.5.2 get_line 函数（逐字符读取一行）

```cpp
int get_line(int sock, char *buf)
{
    char ch = '\0';
    int i = 0;
    int ret = 0;

    // 循环条件：缓冲区未满 且 尚未读到换行符
    while(i < SIZE && ch != '\n')
    {
        // 每次只读1字节，效率较低但对HTTP报文解析足够
        ret = recv(sock, &ch, 1, 0);

        if(ret > 0 && ch == '\r')       // 读到回车符\r
        {
            // 用MSG_PEEK窥探下一个字符，但不从缓冲区取走
            int s = recv(sock, &ch, 1, MSG_PEEK);
            if(s > 0 && ch == '\n')     // 如果下一个确实是\n
            {
                recv(sock, &ch, 1, 0);  // 正式读走这个\n
            } else {
                ch = '\n';              // 否则将\r替换为\n统一处理
            }
        }

        buf[i] = ch;    // 将字符放入缓冲区
        i++;
    }
    buf[i] = '\0';      // 字符串终止符
    return i;           // 返回实际读取的字符数
}
```

**走读要点**：
- HTTP协议规定行结束符为 `\r\n`（CRLF），但为了兼容某些不规范的客户端，代码也处理了单独 `\r` 的情况。
- `MSG_PEEK` 的作用：查看缓冲区中的数据但不移除，这样可以根据下一个字符的值决定是否消费它。
- 每次 `recv` 只读1字节，这是最简单的实现方式。生产环境通常会一次性读入大块数据再在内存中解析，以减少系统调用次数。
- 返回值 `i` 可用于判断是否为空行（`i==1 && buf[0]=='\n'` 表示读到空行，即首部结束标志）。

#### 2.5.3 clear_header 函数

```cpp
static void clear_header(int sock)
{
    char buf[4096] = "";
    int ret = 0;
    do {
        ret = get_line(sock, buf);      // 逐行读取
    } while (ret != 1 && strcmp(buf, "\n") != 0);
    // 直到读到空行（仅含\n的一行），表示首部已全部读完丢弃
}
```

**走读要点**：
- 当服务器只需要请求行而不关心其余首部时，必须把剩余的首部行全部读走，否则这些数据会残留在socket缓冲区中，干扰后续的Body读取。
- `static` 关键字限制函数只在当前文件可见，属于内部实现细节。

#### 2.5.4 show_404 函数

```cpp
static void show_404(int sock)
{
    clear_header(sock);  // 先把请求的剩余首部读完丢弃

    // 发送状态行
    const char *msg = "HTTP/1.1 404 Not Found\r\n";
    send(sock, msg, strlen(msg), 0);
    // 发送空行分隔首部和Body（这一步极其重要！缺少则浏览器无法正确解析）
    send(sock, "\r\n", strlen("\r\n"), 0);

    // 获取404页面的文件大小
    struct stat st;
    stat("../wwwroot/404.html", &st);

    // 打开404页面文件
    int fd = open("../wwwroot/404.html", O_RDONLY);
    if(fd == -1) { perror("open 404 error"); return; }

    // 用sendfile零拷贝发送整个文件内容
    sendfile(sock, fd, NULL, st.st_size);
    close(fd);
}
```

**走读要点**：
- `send(sock, "\r\n", ...)` 发送的空行是HTTP协议要求的"首部与Body分隔符"，遗漏此行是最常见的初学者错误。
- `sendfile()` 在内核空间直接完成文件到socket的数据拷贝，避免了用户态→内核态的多次切换，性能优于 `read()+write()`。
- `stat()` 获取文件信息主要是为了得到 `st.st_size`（文件大小），`sendfile` 需要知道发送多少字节。

#### 2.5.5 echo_www 函数（正常页面响应）

```cpp
static int echo_www(int sock, const char *path, size_t s)
{
    int fd = open(path, O_RDONLY);
    if(fd == -1) { perror("open error"); return -1; }

    // 发送200 OK状态行
    const char *msg = "HTTP/1.1 200 OK\r\n";
    send(sock, msg, strlen(msg), 0);
    // 发送空行
    send(sock, "\r\n", strlen("\r\n"), 0);

    // 零拷贝发送文件
    if(sendfile(sock, fd, NULL, s) == -1)
    {
        echo_error(sock, 500);   // sendfile失败则返回500错误
        return -1;
    }

    close(fd);
    return 0;
}
```

**走读要点**：
- 此函数是最简化的HTTP响应实现：只有状态行+空行+文件内容，没有Content-Type、Content-Length等首部。
- 缺少Content-Type意味着浏览器需要根据内容自行推断MIME类型，对于HTML文件通常能正确识别，但对于CSS/JS文件可能导致解析错误。
- 生产级实现应该加上 `Content-Type: text/html\r\n` 和 `Content-Length: %zu\r\n` 首部。

#### 2.5.6 handle_request 函数（处理POST/带参数GET）

```cpp
static int handle_request(int sock, const char *method,
                          const char *path, const char *querry_string)
{
    char line[SIZE] = "";
    int ret = 0;
    int content_len = -1;

    if(strcasecmp(method, "GET") == 0)
    {
        clear_header(sock);     // GET请求：清空剩余首部即可
    } else {
        // POST请求：遍历首部找到Content-Length
        do {
            ret = get_line(sock, line);
            if(strncasecmp(line, "content-length", 14) == 0)
            {
                content_len = atoi(line + 16);  // "Content-Length: 35\r\n"
                                                 // 偏移16跳过"Content-Length: "
            }
        } while(ret != 1 && strcmp(line, "\n") != 0);
    }

    // 打印调试信息
    printf("method = %s\n", method);
    printf("query_string = %s\n", querry_string);
    printf("content_len = %d\n", content_len);

    char req_buf[4096] = "";
    // POST请求：读取Body数据
    if(strcasecmp(method, "POST") == 0)
    {
        int len = recv(sock, req_buf, content_len, 0);
        printf("len = %d\n", len);
        printf("req_buf = %s\n", req_buf);
    }

    // 发送响应首部（含空行）
    const char *msg = "HTTP/1.1 200 OK\r\n\r\n";
    send(sock, msg, strlen(msg), 0);

    // 交给业务层处理
    parse_and_process(sock, querry_string, req_buf);

    return 0;
}
```

**走读要点**：
- POST请求的Body长度由 `Content-Length` 首部决定，必须先解析首部才能得到Body大小。
- `line + 16` 是硬编码偏移量，假设首部格式严格为 `"Content-Length: "` （14个字母+冒号+空格=16字符）。如果客户端发送的格式稍有不同（如多余空格），就会解析出错。
- `recv(sock, req_buf, content_len, 0)` 一次性读取Body，前提是content_len不超过4096。如果Body更大，需要循环读取。

#### 2.5.7 handler_msg 函数（请求处理总入口）

这是整个HTTP服务器的核心调度函数，流程如下：

```
MSG_PEEK预览 → get_line读请求行 → 解析method → 解析url → 
拼接path → stat检查文件 → 分支处理(GET/POST/404) → close
```

**关键代码段走读**：

```cpp
// 第一步：MSG_PEEK预览数据（不消费），用于调试打印
recv(sock, del_buf, SIZE, MSG_PEEK);

// 第二步：正式读取请求行
char buf[SIZE] = "";
int count = get_line(sock, buf);
// 此时buf = "GET /index.html HTTP/1.1\n"

// 第三步：解析请求方法（空格前的字符串）
char method[32] = "";
int k = 0, i = 0;
for(i; i < count; i++) {
    if(isspace(buf[i])) break;    // 遇到空格停止
    method[k++] = buf[i];         // 逐字符复制
}
method[k] = '\0';
// 此时method = "GET"

// 第四步：跳过空格
while(isspace(buf[i]) && i < SIZE) i++;

// 第五步：验证方法是否为GET或POST
if(strcasecmp(method,"GET")!=0 && strcasecmp(method,"POST")!=0)
{
    close(sock); return -1;       // 不支持的方法直接关闭
}

// 第六步：解析URL（空格前、问号前的部分）
char url[SIZE] = "";
int t = 0;
char *querry_string = NULL;
for(i; i < SIZE; i++) {
    if(isspace(buf[i])) break;
    if(buf[i] == '?') {           // 遇到问号，分离URL和查询串
        querry_string = &url[t];
        querry_string++;          // 指向问号后面的字符
        url[t] = '\0';           // URL在此截断
    } else {
        url[t] = buf[i];
    }
    t++;
}
url[t] = '\0';
// 例如 "/post.html?data1=1&data2=2" → url="/post.html", querry_string="data1=1&data2=2"

// 第七步：拼接服务器文件路径
char path[SIZE] = "";
sprintf(path, "../wwwroot%s", url);
if(path[strlen(path)-1] == '/')
    strcat(path, "index.html");   // 目录请求默认返回index.html

// 第八步：检查文件是否存在
struct stat st;
if(stat(path, &st) == -1) {
    echo_error(sock, 404);        // 文件不存在→404
    close(sock); return -1;
}

// 第九步：根据请求类型分发处理
if(need_handle == 1) {
    handle_request(sock, method, path, querry_string);
} else {
    clear_header(sock);
    echo_www(sock, path, st.st_size);
}

close(sock);
return 0;
```

**走读要点**：
- `MSG_PEEK` 预览不影响后续的正常读取，纯粹是为了调试输出。`#if 1` 编译开关可以随时关闭这段调试代码。
- URL解析中对 `?` 的处理技巧：先在url数组中预留位置，遇到 `?` 后将该位置设为 `\0` 截断URL，同时让 `querry_string` 指向下一个位置。
- `need_handle` 标志位的设计：POST请求一律需要手动处理；GET请求如果带了查询参数（`?key=value`）也需要手动处理；只有纯GET静态文件请求才走 `echo_www` 快速路径。
- 注意 `handler_msg` 末尾和 `msg_request` 中都有 `close(sock)`，实际上 `handler_msg` 内部的 close 已经关闭了fd，外层的 close 是对同一个fd再次调用，会返回 EBADF 错误但不影响程序运行。这是代码的一个小瑕疵。

---

### 2.6 custom_handle.cpp 业务逻辑逐行走读

```cpp
#include "custom_handle.h"
#include <myhead.h>

#define KB 1024
#define HTML_SIZE (64 * 1024)    // 64KB回复缓冲区

// ========== 处理求和请求 ==========
static int handle_add(int sock, const char *req_buf)
{
    int num1, num2;
    // 从POST Body中解析两个数字
    // req_buf格式类似: "data1=12data2=34"
    sscanf(req_buf, "\"data1=%ddata2=%d\"", &num1, &num2);

    char reply_buf[HTML_SIZE] = "";
    sprintf(reply_buf, "%d", num1 + num2);    // 将结果转为字符串

    send(sock, reply_buf, strlen(reply_buf), 0);  // 发送纯文本结果
    return 0;
}

// ========== 处理登录请求 ==========
int handle_login(int sock, char *req_buf)
{
    char reply_buf[HTML_SIZE] = "";

    // 解析表单数据: "username=admin&password=123456"
    char *uname = strstr(req_buf, "username=");
    uname += strlen("username=");              // 跳过键名，指向值

    char *ptr = strstr(req_buf, "password=");
    *(ptr - 1) = '\0';                         // 将&替换为\0，截断用户名

    char *passwd = ptr + strlen("password=");  // 指向密码值

    // 简单验证：账号和密码相同则视为登录成功
    if(strcmp(uname, passwd) == 0)
    {
        // 返回JavaScript代码：保存用户名到localStorage + 跳转到首页
        sprintf(reply_buf,
            "<script>localStorage.setItem('usr_user_name', '%s');</script>", uname);
        strcat(reply_buf,
            "<script>window.location.href='/index.html';</script>");

        send(sock, reply_buf, strlen(reply_buf), 0);
    }
    return 0;
}

// ========== 业务分发入口 ==========
int parse_and_process(int sock, const char *querry_string, char *req_buf)
{
    // 根据Body内容判断是哪个业务
    if(strstr(req_buf, "data1=") && strstr(req_buf, "data2="))
    {
        return handle_add(sock, req_buf);       // 求和业务
    }
    else if(strstr(req_buf, "username=") && strstr(req_buf, "password="))
    {
        return handle_login(sock, req_buf);     // 登录业务
    }
    // 其他请求暂不处理
    return 0;
}
```

**走读要点**：
- `sscanf` 的格式串 `"\"data1=%ddata2=%d\""` 匹配前端 `JSON.stringify(data)` 产生的带引号格式。如果前端发送格式变化，此处会解析失败。
- 登录验证极度简化（账号==密码即成功），仅用于演示POST数据处理流程。
- 登录成功后返回的不是HTML页面而是JavaScript脚本，通过 `window.location.href` 实现客户端跳转。这是一种AJAX风格的响应方式。
- `parse_and_process` 通过字符串匹配来路由业务请求，在生产环境中应使用更结构化的路由机制（如正则匹配或路由表）。

---

### 2.7 wwwroot 资源文件说明

| 文件 | 用途 | 关键技术点 |
|------|------|-----------|
| index.html | 首页，GET请求默认返回 | 最简HTML结构 |
| 404.html | 资源不存在时的错误页面 | 状态码与页面配合 |
| login.html | 登录表单，演示POST请求 | form method="post"、CSS样式 |
| post.html | AJAX求和，演示异步POST | XMLHttpRequest、JSON序列化 |
| 样式表.css | 外部CSS样式表 | 渐变背景、Flex布局 |

**post.html 核心逻辑走读**：
```javascript
function sendPOSTRequest() {
    var xhr = new XMLHttpRequest();     // 创建异步请求对象
    data = "data1=" + document.getElementById("data1").value
         + "data2=" + document.getElementById("data2").value;
    xhr.open("POST", url, true);        // 配置：POST方法、异步模式
    xhr.onreadystatechange = function() {
        if(xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById("sum").value = xhr.responseText;
        }
    };
    xhr.send(JSON.stringify(data));     // 发送JSON格式的Body
}
```

点击"求和"按钮 → JS收集两个输入框的值 → 拼接为 `data1=Xdata2=Y` → JSON序列化后POST到服务器 → 服务器解析并计算求和 → 返回结果文本 → JS将结果显示在第三个输入框中。整个过程页面无刷新，体现了BS架构下前后端交互的典型模式。

---

## 三、对比表格汇总

### 3.1 GET vs POST 对比

| 维度 | GET | POST |
|------|-----|------|
| 数据位置 | URL查询串（?后面） | 请求Body |
| 数据长度限制 | 受URL长度限制（约2KB） | 理论上无限制（受Content-Length） |
| 安全性 | 参数暴露在URL中 | 参数在Body中（但仍需HTTPS加密） |
| 缓存 | 可被浏览器缓存 | 默认不缓存 |
| 幂等性 | 幂等（多次请求结果相同） | 非幂等（可能产生副作用） |
| 书签 | 可收藏 | 不可收藏 |
| 本章代码处理 | echo_ww直接返回文件 | handle_request解析Body后调业务函数 |

### 3.2 HTTP版本核心差异对比（详见1.4节表格）

### 3.3 五种常见状态码对比

| 状态码 | 类别 | 触发条件 | 服务器动作 | 客户端动作 |
|--------|------|---------|-----------|-----------|
| 200 | 成功 | 请求正常处理 | 返回请求的资源 | 渲染页面 |
| 304 | 重定向 | 资源未修改 | 不返回Body | 使用本地缓存 |
| 400 | 客户端错误 | 请求语法错误 | 返回错误信息 | 提示用户修正 |
| 404 | 客户端错误 | 资源不存在 | 返回404页面 | 显示未找到 |
| 500 | 服务器错误 | 服务器内部异常 | 返回错误信息 | 提示稍后重试 |

---

## 四、两套速查表

### 4.1 精简版速查表（一页速览）

```
【HTTP请求报文】
GET /path HTTP/1.1\r\n
Host: xxx\r\n
\r\n

【HTTP响应报文】
HTTP/1.1 200 OK\r\n
\r\n
<body>

【状态码速记】
200=成功  304=未修改  400=语法错  404=找不到  500=服务器炸

【请求方法速记】
GET=获取  POST=提交  HEAD=只看头  PUT=替换  DELETE=删除

【服务器三步曲】
init_server(socket→bind→listen) → accept循环 → handler_msg(解析→响应)

【版本一句话】
1.0短连接串行 → 1.1长连接管道 → 2.0二进制并发 → 3.0 QUIC无阻塞
```

### 4.2 详细版速查表

#### 请求报文模板
```
<方法> <URL> <版本>\r\n
Host: <主机名:端口>\r\n
Content-Type: <MIME类型>\r\n        ← POST时必填
Content-Length: <字节数>\r\n        ← POST时必填
\r\n
<实体主体>                           ← GET时通常为空
```

#### 响应报文模板
```
<版本> <状态码> <短语>\r\n
Content-Type: <MIME类型>\r\n
Content-Length: <字节数>\r\n
\r\n
<实体主体>
```

#### MIME类型对照
| 文件类型 | Content-Type |
|---------|-------------|
| .html | text/html |
| .css | text/css |
| .js | application/javascript |
| .json | application/json |
| .png | image/png |
| .jpg | image/jpeg |
| .txt | text/plain |

#### 关键API签名
```c
// 创建套接字
int socket(int domain, int type, int protocol);
// AF_INET, SOCK_STREAM, 0

// 绑定地址
int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);

// 监听
int listen(int sockfd, int backlog);

// 接受连接
int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);

// 发送数据
ssize_t send(int sockfd, const void *buf, size_t len, int flags);

// 接收数据
ssize_t recv(int sockfd, void *buf, size_t len, int flags);
// flags: 0=阻塞读取并消费, MSG_PEEK=窥探不消费

// 零拷贝发送文件
ssize_t sendfile(int out_fd, int in_fd, off_t *offset, size_t count);

// 端口复用
setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));

// 创建线程
int pthread_create(pthread_t *tid, const pthread_attr_t *attr,
                   void *(*start_routine)(void *), void *arg);

// 分离线程
int pthread_detach(pthread_t tid);
```

#### 服务器初始化清单
1. `socket()` 创建TCP套接字
2. `setsockopt(SO_REUSEADDR)` 端口复用
3. `bind()` 绑定IP和端口
4. `listen()` 启动监听
5. `accept()` 循环接收连接
6. `pthread_create()` 为每个连接创建处理线程
7. `pthread_detach()` 分离线程避免资源泄漏

---

## 五、易错点速查卡

| 错误现象 | 错误原因 | 正确写法 | 后果 |
|---------|---------|---------|------|
| 浏览器显示源码而非渲染页面 | 响应缺少Content-Type首部或值不正确 | 添加 `Content-Type: text/html\r\n` | 浏览器按纯文本展示 |
| 浏览器一直加载转圈 | 响应首部和Body之间缺少空行 | 首部最后发送 `\r\n\r\n` | 浏览器等待Body起始标志 |
| 服务器重启报Address in use | 未设置SO_REUSEADDR | `setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse))` | 需等60秒才能重启 |
| 客户端读到乱码/错位数据 | 线程传参用了栈变量地址`&sock` | 用堆分配 `new int(sock)` + 线程内 `delete` | 数据竞争导致随机bug |
| fd泄漏，accept最终失败 | 线程处理完未close(sock) | 线程函数末尾 `close(sock)` | 耗尽文件描述符上限 |
| POST Body读不完整 | 未先解析Content-Length就直接recv | 先遍历首部找Content-Length，再按长度recv | 读到不完整数据或阻塞 |
| 404页面不显示 | 路径拼写错误或工作目录不对 | 确认相对路径基准（build目录下用`../wwwroot`） | 用户看到空白或连接重置 |
| sendfile返回-1 | 文件大小为0或fd无效 | 先用stat确认文件存在且大小>0 | 客户端收到不完整响应 |
| 中文页面乱码 | HTML缺少charset声明 | `<meta charset="UTF-8">` + 文件保存为UTF-8 | 浏览器用错误编码解码 |
| 请求方法判断失败 | 用strcmp而非strcasecmp | `strcasecmp(method, "GET")` 忽略大小写 | 某些客户端发小写get被拒绝 |

---

## 六、常见陷阱专题

### 陷阱1：HTTP响应缺少空行分隔首部和主体

**错误写法**：
```cpp
const char *msg = "HTTP/1.1 200 OK\r\n";
send(sock, msg, strlen(msg), 0);
// 忘记发送空行，直接发Body
sendfile(sock, fd, NULL, st.st_size);
```

**后果**：浏览器无法区分哪里是首部、哪里是Body。有的浏览器会将整个响应当作首部等待更多数据（表现为一直loading），有的会把首部文本显示在页面上。

**正确写法**：
```cpp
const char *msg = "HTTP/1.1 200 OK\r\n";
send(sock, msg, strlen(msg), 0);
send(sock, "\r\n", strlen("\r\n"), 0);    // ← 空行分隔，绝对不能省
sendfile(sock, fd, NULL, st.st_size);
```

**记忆口诀**："响应两换行，首部身体分"

**原理**：HTTP协议规定首部行结束后必须有一个空行（`\r\n`），这是解析器判断首部结束的唯一标志。没有这个空行，解析器会一直等待更多首部行。

---

### 陷阱2：Content-Type与实际文件类型不匹配

**错误写法**：
```cpp
// 返回CSS文件时使用了text/html
const char *header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n";
```

**后果**：浏览器收到CSS文件但被告知是HTML类型，会以HTML解析器处理CSS内容，导致样式完全不生效，控制台报 MIME type mismatch 错误。

**正确写法**：
```cpp
// 根据文件后缀动态设置Content-Type
const char *get_content_type(const char *path) {
    if (strstr(path, ".html")) return "text/html";
    if (strstr(path, ".css"))  return "text/css";
    if (strstr(path, ".js"))   return "application/javascript";
    if (strstr(path, ".png"))  return "image/png";
    if (strstr(path, ".jpg"))  return "image/jpeg";
    return "application/octet-stream";  // 未知类型用二进制流
}
```

**记忆口诀**："类型要对号，否则浏览器懵"

**原理**：浏览器依赖Content-Type决定用什么解析器处理响应Body。类型错误等于告诉浏览器用错了工具。

---

### 陷阱3：多线程处理请求时忘记close通信fd

**错误写法**：
```cpp
void *msg_request(void *arg) {
    int sock = *(int *)arg;
    delete (int *)arg;
    handler_msg(sock);
    // 忘记close(sock)!
    return NULL;
}
```

**后果**：每个请求处理完后fd不会被释放。Linux默认每个进程最多打开1024个fd，当并发请求累积到上限后，`accept()` 返回 EMFILE 错误，服务器彻底无法接受新连接。用 `lsof -p <pid>` 可以看到大量CLOSE_WAIT状态的fd。

**正确写法**：
```cpp
void *msg_request(void *arg) {
    int sock = *(int *)arg;
    delete (int *)arg;
    handler_msg(sock);
    close(sock);        // ← 必须关闭！
    return NULL;
}
```

**进阶方案（RAII封装）**：
```cpp
class SocketGuard {
    int fd_;
public:
    explicit SocketGuard(int fd) : fd_(fd) {}
    ~SocketGuard() { if (fd_ >= 0) close(fd_); }
    int get() const { return fd_; }
    // 禁止拷贝
    SocketGuard(const SocketGuard&) = delete;
    SocketGuard& operator=(const SocketGuard&) = delete;
};
```

**记忆口诀**："谁accept谁close，线程用完要归还"

---

## 七、新手最常问的5个问题

### Q1：为什么我的服务器启动后浏览器访问显示空白？
**答**：最常见原因是HTTP响应缺少空行 `\r\n\r\n`。浏览器收到了状态行但没有看到空行分隔符，就一直等待更多首部数据。检查 `echo_www` 和 `show_404` 函数中是否在状态行后发送了 `"\r\n"`。另外确认服务器监听的端口号和浏览器访问的端口号一致。

### Q2：为什么服务器关闭后再启动总是报 "Address already in use"？
**答**：TCP连接关闭后会进入 TIME_WAIT 状态，持续约60秒。在此期间同一端口不能被重新绑定。解决方法是在 `bind()` 之前调用 `setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse))`。本章源码 `init_server` 函数中已包含此设置。

### Q3：GET和POST到底有什么区别？什么时候用哪个？
**答**：GET用于获取资源，参数放在URL中，适合查询操作；POST用于提交数据，参数放在Body中，适合创建/修改操作。经验法则：不改变服务器状态用GET，会改变服务器状态用POST。在本章服务器中，访问静态页面用GET，登录和求和用POST。

### Q4：为什么pthread_create传参要用new int(sock)而不能直接传&sock？
**答**：`sock` 是main函数while循环中的局部变量，每次循环都会被accept的新返回值覆盖。如果用 `&sock`，子线程可能在还没读取到值的时候，主线程就已经把sock改成了下一个连接的fd。用 `new int(sock)` 在堆上创建独立的副本，每个线程拥有自己的fd值，互不干扰。

### Q5：HTTP/1.1明明有管道化，为什么还说它有队头阻塞？
**答**：HTTP/1.1的管道化允许客户端在同一连接上连续发送多个请求（解决了"请求队头阻塞"），但服务器必须按照接收请求的顺序依次返回响应。如果第一个请求处理很慢，后面的请求即使已经处理完也必须排队等待。这就是"响应队头阻塞"。HTTP/2.0通过stream机制彻底解决了这个问题，允许响应乱序返回。

---

## 八、代码自测清单

学完本章后，你应该能独立完成以下任务：

- [ ] 手写一个简单的HTTP响应报文（含状态行、首部、空行、Body）
- [ ] 解析HTTP GET请求，提取请求方法和URL路径
- [ ] 根据URL路径返回对应的文件内容，或返回404页面
- [ ] 用多线程（pthread_create + pthread_detach）处理并发HTTP请求
- [ ] 说出HTTP 1.0/1.1/2.0/3.0的核心区别（至少3点）
- [ ] 解释为什么HTTP响应必须有 `\r\n\r\n` 空行
- [ ] 用curl -v命令观察完整的HTTP请求/响应报文
- [ ] 解释SO_REUSEADDR的作用及为什么开发时必须设置
- [ ] 区分GET和POST的使用场景
- [ ] 解释MSG_PEEK和MSG_WAITALL的区别

---

## 九、复习计划

| 时间节点 | 复习内容 | 复习方式 |
|---------|---------|---------|
| 1天后 | HTTP报文格式、状态码、请求方法 | 默写请求/响应报文模板 + 用curl -v验证 |
| 3天后 | 服务器源码架构、版本对比表 | 重新编译运行服务器 + 浏览器测试GET/POST/404 |
| 7天后 | 全章知识体系回顾 | 看树状图回忆 + 做4道练习题 + 重读代码走读部分 |
| 14天后 | 综合应用 | 尝试给服务器添加一个新功能（如支持CSS文件的Content-Type） |
| 30天后 | 面试准备 | 回顾常见陷阱专题 + 新手5问 + 面试题扩展 |

**复习节奏建议**：
- 每天花10分钟看一遍精简版速查表
- 每周动手运行一次服务器代码，用浏览器实际测试
- 遇到不理解的地方回到详细版速查表和代码走读部分查阅

---

## 十、树状图（全章知识体系）

```
HTTP服务器
├── Web基础概念
│   ├── 万维网(WWW)
│   │   ├── 超文本与超链接
│   │   └── BS模型(浏览器-服务器)
│   ├── URL统一资源定位符
│   │   ├── 协议(http/https)
│   │   ├── 主机名(域名/IP)
│   │   ├── 端口号(默认80)
│   │   └── 路径(/index.html)
│   └── HTML基础
│       ├── 标签(单标签/双标签)
│       ├── 常用标签(h1/p/div/input/a/form)
│       └── 文档结构(DOCTYPE/html/head/body)
│
├── HTTP协议详解
│   ├── 协议特点
│   │   ├── 面向事务
│   │   ├── 可靠(TCP)
│   │   ├── 客户端发起/服务器响应
│   │   ├── 无状态(Cookie/Session弥补)
│   │   └── 无连接(1.0)/长连接(1.1)
│   ├── 版本演进
│   │   ├── 1.0: 短连接+串行
│   │   ├── 1.1: 长连接+管道化(响应队头阻塞)
│   │   ├── 2.0: HPACK+stream并发+服务器推送
│   │   ├── 3.0: QUIC(UDP)+无队头阻塞
│   │   └── HTTPS: TLS加密
│   ├── 请求报文
│   │   ├── 请求行(方法+URL+版本)
│   │   ├── 首部行(Host/Content-Type/Length)
│   │   ├── 实体主体(GET空/POST有数据)
│   │   └── 8种方法(GET/POST/HEAD/PUT/DELETE/OPTIONS/TRACE/CONNECT)
│   └── 响应报文
│       ├── 状态行(版本+状态码+短语)
│       ├── 五类状态码(1xx/2xx/3xx/4xx/5xx)
│       └── 实体主体(文件内容/错误页面)
│
└── HTTP服务器实现
    ├── 架构设计
    │   ├── main.cpp: 主循环+accept+线程创建
    │   ├── http.cpp: TCP初始化+协议解析+响应构造
    │   └── custom_handle.cpp: 业务逻辑(求和/登录)
    ├── 核心函数
    │   ├── init_server: socket→bind→listen
    │   ├── get_line: 逐字符读取一行(处理\r\n)
    │   ├── handler_msg: 请求解析总入口
    │   ├── echo_www: 静态文件响应
    │   ├── show_404: 404错误页面
    │   ├── handle_request: POST/带参GET处理
    │   └── parse_and_process: 业务分发
    ├── 关键技术
    │   ├── SO_REUSEADDR端口复用
    │   ├── MSG_PEEK窥探数据
    │   ├── sendfile零拷贝发送
    │   ├── pthread_create+detach多线程
    │   └── new int(sock)堆传参防竞争
    └── 测试验证
        ├── curl -v观察报文
        ├── 浏览器访问静态页面
        ├── POST表单登录
        └── AJAX异步求和
```

---

## 十一、三条随身速记口诀

1. **"请三响三空行隔"**：请求报文三部分组成，响应报文三部分组成，首部和Body之间用空行分隔。

2. **"一二三零步步快"**：HTTP 1.0短连接、1.1长连接、2.0多路复用、3.0 QUIC零阻塞，每个版本都比上一个更快。

3. **"建绑听接创分关"**：服务器七步口诀——建(socket)、绑(bind)、听(listen)、接(accept)、创(pthread_create)、分(pthread_detach)、关(close)。

---

## 十二、练习题（答案留空）

### 题目1（★ 基础）
**考察知识点**：HTTP响应报文格式

请手写一个完整的HTTP响应报文，要求返回一个包含文本 "Hello World" 的HTML页面。报文必须包含状态行、必要的首部行、空行和实体主体。

你的答案：
```
_______________________________________________
_______________________________________________
_______________________________________________
_______________________________________________
_______________________________________________
```

---

### 题目2（★★ 理解）
**考察知识点**：HTTP请求解析、URL提取

给定以下HTTP请求报文的第一行：
```
GET /search?q=hello&page=2 HTTP/1.1
```
请写出：(1) 请求方法 (2) URL路径 (3) 查询字符串 (4) 如果使用本章服务器的逻辑，拼接后的文件路径是什么？

你的答案：
```
(1) ____________________________________________
(2) ____________________________________________
(3) ____________________________________________
(4) ____________________________________________
```

---

### 题目3（★★★ 应用）
**考察知识点**：多线程HTTP服务器、fd管理

下面的代码有一个严重的bug，请找出并改正，同时解释为什么这个bug会导致问题：

```cpp
void *handle_client(void *arg) {
    int sock = *(int *)arg;
    handler_msg(sock);
    return NULL;
}

int main() {
    int lis_sock = init_server(8080);
    while (1) {
        int sock = accept(lis_sock, NULL, NULL);
        pthread_t tid;
        pthread_create(&tid, NULL, handle_client, &sock);
    }
    return 0;
}
```

你的答案：
```
Bug位置：_______________________________________
Bug原因：_______________________________________
改正方案：_____________________________________
_______________________________________________
```

---

### 题目4（★★★★ 综合）
**考察知识点**：HTTP协议+服务器实现+版本差异+安全性

假设你需要为本章的HTTP服务器添加以下功能：当客户端请求 `/api/data` 路径时，服务器返回JSON格式的响应 `{"status":"ok","count":42}`。

请回答：
(1) 应该在哪个文件的哪个函数中添加路由判断？
(2) 写出完整的HTTP响应报文（包括正确的Content-Type）
(3) 如果要支持HTTPS，需要在服务器架构中增加什么组件？TLS握手发生在TCP握手的什么时机？
(4) 如果将此服务器升级为HTTP/2.0，最大的架构变化是什么？

你的答案：
```
(1) ____________________________________________
_______________________________________________
(2) ____________________________________________
_______________________________________________
_______________________________________________
(3) ____________________________________________
_______________________________________________
(4) ____________________________________________
_______________________________________________
```

---

## 十三、知识蒸馏

HTTP服务器=TCP通信+解析请求报文+按URL找文件+构造响应报文发回去，是Web的技术基石。

---

## 十四、错题记录表

> 使用说明：完成练习题后，将自己的错误填入下表。每次复习时优先看此表。

| 题号 | 题目简述 | 我的错误答案 | 正确答案 | 错误原因 | 涉及知识点 | 复习建议 |
|------|---------|-------------|---------|---------|-----------|---------|
| 1 | 手写HTTP响应报文 | （待填写） | （待批改） | （待分析） | 响应报文格式 | 建议1天后复习 |
| 2 | 解析GET请求URL | （待填写） | （待批改） | （待分析） | 请求行解析 | 建议1天后复习 |
| 3 | 多线程fd管理bug | （待填写） | （待批改） | （待分析） | 线程安全+fd生命周期 | 建议3天后复习 |
| 4 | 综合扩展题 | （待填写） | （待批改） | （待分析） | 协议+架构+安全+版本 | 建议7天后复习 |

---

## 附录A：术语中英对照表

| 中文术语 | 英文术语 | 缩写 |
|---------|---------|------|
| 万维网 | World Wide Web | WWW/Web |
| 统一资源定位符 | Uniform Resource Locator | URL |
| 超文本传输协议 | HyperText Transfer Protocol | HTTP |
| 超文本标记语言 | HyperText Markup Language | HTML |
| 浏览器-服务器模型 | Browser-Server Model | B/S |
| 传输控制协议 | Transmission Control Protocol | TCP |
| 用户数据报协议 | User Datagram Protocol | UDP |
| 传输层安全协议 | Transport Layer Security | TLS |
| 安全超文本传输协议 | HTTP Secure | HTTPS |
| 快速UDP互联网连接 | Quick UDP Internet Connections | QUIC |
| 头部压缩算法 | Header Compression for HTTP/2 | HPACK |
| 多路复用 | Multiplexing | — |
| 队头阻塞 | Head-of-Line Blocking | HoL |
| 套接字 | Socket | — |
| 文件描述符 | File Descriptor | fd |
| 端口复用 | Socket Reuse Address | SO_REUSEADDR |
| 零拷贝 | Zero-Copy | — |
| 守护进程 | Daemon | — |
| 往返时间 | Round-Trip Time | RTT |
| 应用编程接口 | Application Programming Interface | API |
| 多用途互联网邮件扩展 | Multipurpose Internet Mail Extensions | MIME |
| 跨域资源共享 | Cross-Origin Resource Sharing | CORS |
| 通用网关接口 | Common Gateway Interface | CGI |

---

## 附录B：curl实操命令参考

```bash
# 查看完整的HTTP请求和响应报文
curl -v http://localhost:8080/index.html

# 发送GET请求并显示响应头
curl -I http://localhost:8080/index.html

# 发送POST请求
curl -X POST -d "username=admin&password=admin" http://localhost:8080/login.html

# 指定端口访问
curl http://192.168.1.100:8080/post.html

# 只获取响应体（静默模式）
curl -s http://localhost:8080/index.html

# 保存响应到文件
curl -o output.html http://localhost:8080/index.html
```

---

## 附录C：HTTP面试题扩展

### 如何实现CGI/FastCGI？
CGI（Common Gateway Interface）是一种让HTTP服务器调用外部程序处理请求的标准接口。服务器fork一个子进程执行CGI脚本，通过环境变量传递请求信息，通过stdin/stdout传递数据。FastCGI是CGI的改进版，使用常驻进程池而非每次fork新进程，通过Unix域套接字通信，避免了频繁的进程创建销毁开销。

### 如何处理POST表单数据？
POST表单有两种编码格式：`application/x-www-form-urlencoded`（键值对用&连接，特殊字符URL编码）和 `multipart/form-data`（用于文件上传，有boundary分隔各部分）。本章服务器只处理了前者，解析方式是先读Content-Length确定Body大小，再recv读取Body，然后用字符串查找提取键值对。

### 如何支持Keep-Alive？
HTTP/1.1默认启用Keep-Alive。服务器需要在响应头中添加 `Connection: keep-alive`，并在处理完一个请求后不关闭连接，继续读取下一个请求。这需要将本章的"一连接一线程一请求"模型改为"一连接一线程多请求"的循环模型，在handler_msg外层增加while循环直到客户端发送 `Connection: close` 或超时。

---

> **学习心态自评**（学完后请填写）：
> 1. 我理解本章核心概念的程度：____星（1-5）
> 2. 我能独立写出本章示例代码的程度：____星（1-5）
> 3. 我能识别并避免常见错误的程度：____星（1-5）
> 4. 最需要再复习的3个知识点：________________________

---

*笔记生成完毕。本章前置：第5章网络编程。本章后续：第7章项目实战。*
