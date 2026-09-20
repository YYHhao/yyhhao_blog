# 简介
FastAPI 是一个现代、高性能的 Python Web 框架，用于构建 API。它基于 Starlette（异步 Web 框架）和 Pydantic（数据验证库），结合了异步编程和类型提示，兼顾开发效率与运行性能。

**官方文档**[https://fastapi.org.cn/#interactive-api-docs-upgrade](https://fastapi.org.cn/#interactive-api-docs-upgrade)

# 特点
## 核心优势
易上手、高性能、开发速度快、代码可读性 / 可维护性高、支持异步、自动校验



## 适用场景

* 前后端分离项目的后端 API 开发（如 Vue/React 前端 + FastAPI 后端）；
* 移动端 / 小程序的数据接口开发（APP / 小程序调用的接口）；
* 微服务 / 分布式系统的接口开发（如订单服务、用户服务）；
* 数据可视化 / 自动化工具的接口（如爬虫数据提供接口、数据分析接口）；
* 新手学习 Web 开发（语法简单、反馈及时、实战价值高）。
* 机器学习服务：可将训练好的模型封装为 API，方便前端和其他服务调用。

## 核心特性
除了核心优势，FastAPI 还提供了 Web 开发所需的全功能支持，且都做到了 “简单、高效”：

核心特性	|用途	|新手优先级
---|---|---  
路由系统	|定义接口路径、请求方法（GET/POST/PUT/DELETE）|	必须掌握
参数处理	|路径参数、查询参数、请求体、Cookie/Header|	必须掌握
数据校验	|Pydantic 模型、字段约束、嵌套模型	|必须掌握
响应定制|	状态码、响应模型（过滤字段）、JSON/HTML 响应	|必须掌握
依赖注入	|提取公共逻辑（如登录校验、权限控制）|重点掌握
用户认证	|OAuth2/JWT、API Key、Cookie 认证	|重点掌握
数据库操作	|对接 SQLite/MySQL/PostgreSQL	|必须掌握
文件上传 / 下载	|单文件 / 多文件上传、文件流下载	|了解掌握
跨域处理	|解决前端跨域请求问题（CORS）	|必须掌握
异步编程	|异步函数、异步数据库、异步依赖	|后期掌握
后台任务	|接口返回后执行耗时操作（如发送邮件）	|了解掌握
部署上线	|Gunicorn+Uvicorn、Docker、云服务器	|后期掌握


# 基础应用
## 异步处理
ASGI（Asynchronous Server Gateway Interface）是 Python 异步 Web 服务器和应用程序之间的标准接口。

WSGI vs ASGI 对比：
```
# WSGI 应用（同步）- 传统 Flask 风格
def wsgi_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [b'Hello World']

# ASGI 应用（异步）- FastAPI 风格
async def asgi_app(scope, receive, send):
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [(b'content-type', b'text/plain')],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello World',
    })
```

**适合异步的场景：**

* 数据库操作
* 网络请求（API 调用）
* 文件 I/O 操作
* 长时间等待的操作

**不适合异步的场景：**

* CPU 密集型计算
* 简单的数据处理
* 没有 I/O 等待的操作

## 路由系统

路由系统是 FastAPI 的“骨架”——决定用户访问哪个 URL 能触发哪个功能。可以类比 Python 的“函数调用”：URL 路径像函数名，请求方法像调用方式，二者一起决定执行哪个接口函数。

### 核心知识点

* 使用 `@app.get()`、`@app.post()`、`@app.put()`、`@app.delete()` 声明接口，通常分别用于查询、创建、整体更新、删除资源。
* 同一个路径可以对应不同请求方法，例如 `GET /users` 查询用户，`POST /users` 创建用户。
* 路径中的 `{user_id}` 是动态参数，函数通过同名参数接收。
* 固定路径应放在可能匹配它的动态路径前，例如先声明 `/users/me`，再声明 `/users/{user_id}`。
* 使用 `APIRouter` 按业务组织路由，`prefix` 设置统一前缀，`tags` 设置文档分组，最后通过 `include_router()` 注册。

### 示例：按用户模块组织路由

以下各节示例使用 Python 3.10+ 和 Pydantic v2，每节可单独保存为 `main.py`，不需要把所有示例拼接在一起。基础安装与开发启动命令为：

```bash
pip install "fastapi[standard]"
uvicorn main:app --reload
```

`main:app` 表示加载 `main.py` 中的 `app` 对象。启动后访问 `http://127.0.0.1:8000/docs`，可以填写参数并测试接口。

```python
from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter(prefix="/users", tags=["用户"])


@router.get("/me")
def read_me():
    return {"username": "小明"}


@router.get("/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}


app.include_router(router)
```

访问 `GET /users/me` 返回演示用户，访问 `GET /users/12` 返回 `{"user_id": 12}`。这里的 `/me` 只演示路由匹配，尚未接入登录认证。

## 参数处理

参数处理是接口的“收件窗口”：客户端把信息放在 URL、请求体或请求头里，FastAPI 按声明的位置取出，再传给函数。类比 Python 调用函数时传实参，只是 Web 请求多了几种传递渠道。

### 核心知识点

| 参数来源 | 声明方式 | 常见用途 |
| --- | --- | --- |
| 路径参数 | 路径中的 `{参数名}`，可配合 `Path()` | 指定资源 ID |
| 查询参数 | 不在路径中的普通标量参数，或 `Query()` | 搜索、分页、筛选 |
| JSON 请求体 | Pydantic 模型，或 `Body()` | 提交结构化数据 |
| 请求头 | `Header()` | 传递客户端标识、认证信息 |
| Cookie | `Cookie()` | 读取浏览器保存的会话标识等 |

* `Annotated[类型, 参数配置]` 可以同时表达类型和参数来源、约束。
* 没有默认值的参数通常必填，设置默认值后可以省略；路径参数始终必填。
* `str | None` 表示允许 `None`，还需要 `= None` 才表示可以不传。
* `Header()` 默认把参数名中的下划线转换为连字符，例如 `x_client` 对应 `X-Client`。

### 示例：同时接收多种参数

```python
from typing import Annotated
from fastapi import Cookie, FastAPI, Header, Path, Query
from pydantic import BaseModel

app = FastAPI()


class ItemUpdate(BaseModel):
    name: str


@app.put("/items/{item_id}")
def update_item(
    item_id: Annotated[int, Path(gt=0)],
    item: ItemUpdate,
    notify: Annotated[bool, Query()] = False,
    x_client: Annotated[str | None, Header()] = None,
    session_id: Annotated[str | None, Cookie()] = None,
):
    return {
        "item_id": item_id,
        "name": item.name,
        "notify": notify,
        "client": x_client,
        "has_session_cookie": session_id is not None,
    }
```

发送 `PUT /items/3?notify=true`，JSON 请求体为 `{"name": "键盘"}`，请求头为 `X-Client: web`，未携带 Cookie 时返回：

```json
{"item_id": 3, "name": "键盘", "notify": true, "client": "web", "has_session_cookie": false}
```

## 数据校验

数据校验是接口的“质检员”：参数处理负责取出数据，数据校验负责检查它是否符合要求。例如价格必须大于零、商品名称不能为空，这些规则都可以直接写在模型中。

### 核心知识点

* 继承 `BaseModel` 定义请求结构，字段类型决定数据应当是什么类型。
* 使用 `Field()` 设置约束，如 `gt=0` 表示大于零、`ge=0` 表示大于等于零，`min_length` / `max_length` 限制长度。
* 模型可以嵌套其他模型，也可以使用 `list[模型]` 表示对象列表。
* Pydantic 默认会进行允许的类型转换；字段设置 `strict=True` 可以启用严格类型校验。
* 请求数据不符合声明时，FastAPI 默认返回 `422`，在 `detail` 中说明错误位置；Pydantic v2 模型可通过 `model_dump()` 转为字典。

### 示例：校验商品及其分类

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Category(BaseModel):
    name: str = Field(min_length=1, max_length=20)


class Product(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    price: float = Field(gt=0)
    stock: int = Field(ge=0, strict=True)
    category: Category


@app.post("/products")
def create_product(product: Product):
    return product.model_dump()
```

向 `POST /products` 提交 `{"name": "键盘", "price": 99.9, "stock": 10, "category": {"name": "数码"}}` 会通过校验；将价格改为 `-1`，或将库存改为字符串 `"10"`，都会返回 `422`。

## 响应定制

响应定制是接口的“出货包装”：处理完请求后，需要决定返回哪些字段、使用什么格式、附带什么状态码。类比 Python 函数的返回值，Web 接口还要告诉客户端这次操作是否成功。

### 核心知识点

* 返回字典或列表时，FastAPI 通常会把内容序列化为 JSON。
* `response_model` 声明输出结构，对返回数据进行校验和字段过滤，避免暴露未声明的内部字段。
* `status_code` 设置成功状态码，如 `200` 表示成功、`201` 表示创建成功。
* `HTMLResponse` 返回 HTML，`FileResponse` 返回文件，`StreamingResponse` 返回流式内容。
* 使用 `raise HTTPException(...)` 中断处理并返回错误，例如资源不存在时返回 `404`。

### 示例：过滤用户内部字段

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class UserPublic(BaseModel):
    id: int
    username: str


@app.get("/users/{user_id}", response_model=UserPublic)
def read_user(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"id": 1, "username": "小明", "internal_note": "仅供内部使用"}
```

访问 `GET /users/1` 只返回 `{"id": 1, "username": "小明"}`；访问 `GET /users/2` 返回状态码 `404` 和 `{"detail": "用户不存在"}`。

## 依赖注入

依赖注入像给接口准备“公共工具箱”：分页参数、数据库会话、当前用户等逻辑先封装成函数，由 FastAPI 在调用接口前执行并把结果传进来，避免每个接口重复编写相同代码。

### 核心知识点

* `Depends(函数名)` 声明依赖，传入函数本身，不要写成 `Depends(函数名())`。
* 依赖函数也可以接收查询参数、请求头，甚至依赖其他函数。
* 同一请求中，同一个依赖的结果默认会被复用；这不是跨请求的全局缓存。
* 带有 `yield` 的依赖可以管理资源，并在使用后清理，常用于关闭数据库会话。

### 示例：复用分页参数

```python
from typing import Annotated
from fastapi import Depends, FastAPI, Query

app = FastAPI()


def pagination(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return {"offset": offset, "limit": limit}


@app.get("/items")
def list_items(page: Annotated[dict, Depends(pagination)]):
    items = ["键盘", "鼠标", "显示器"]
    start = page["offset"]
    return {"items": items[start:start + page["limit"]], **page}
```

访问 `GET /items?offset=1&limit=1` 返回 `{"items": ["鼠标"], "offset": 1, "limit": 1}`，其他列表接口也可以复用 `pagination`。

## 用户认证

用户认证是接口的“门禁”：先确认请求者是谁，再决定是否允许进入。认证回答“你是谁”，权限控制回答“你能做什么”，两者通常通过依赖函数组合实现。

### 核心知识点

* API Key 常用于服务间调用，Cookie 会话常用于浏览器登录，Bearer Token 常通过 `Authorization` 请求头传递。
* OAuth2 是授权框架，JWT 是一种令牌格式，两者不是同一个概念。
* FastAPI 的安全组件负责提取凭证并描述认证方式，业务代码仍需验证凭证。
* 验证 JWT 时需要检查签名、有效期等，不能只解码载荷；用户密码应以安全哈希保存。

### 示例：使用 API Key 保护接口

先在启动服务的同一个 PowerShell 窗口设置演示密钥：

```powershell
$env:DEMO_API_KEY = 'local-example-key'
```

```python
import os
import secrets
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader

app = FastAPI()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
expected_key = os.environ["DEMO_API_KEY"]


def verify_key(key: Annotated[str | None, Depends(api_key_header)]):
    if key is None or not secrets.compare_digest(key.encode(), expected_key.encode()):
        raise HTTPException(status_code=401, detail="API Key 无效")
    return key


@app.get("/private", dependencies=[Depends(verify_key)])
def read_private():
    return {"message": "认证通过"}
```

启动后，在 `/docs` 的 `Authorize` 中填写 `local-example-key`，再请求 `GET /private`，返回 `{"message": "认证通过"}`；未提供密钥或密钥错误时返回 `401`。该示例演示共享密钥认证，不包含用户注册和登录流程；部署时应替换演示密钥并通过 HTTPS 传输。

## 数据库操作

数据库是接口的“长期记忆”：普通变量会随着程序退出而消失，数据库可以持续保存用户、文章、订单等数据。FastAPI 负责接收请求，数据库库或 ORM 负责完成查询和写入。

### 核心知识点

* FastAPI 不限定数据库，可以对接 SQLite、MySQL、PostgreSQL 等，常搭配 SQLAlchemy 或 SQLModel。
* `Engine` 管理数据库连接，`Session` 管理数据库交互，通常通过依赖为请求创建会话。
* `add()` 把对象加入会话，`commit()` 提交事务，`refresh()` 重新读取数据库生成的字段。
* 输入模型和数据库表模型可以分开，避免客户端随意指定主键等内部字段。
* 同步数据库操作适合普通 `def` 路由；异步接口应搭配异步驱动和异步会话，避免直接执行阻塞调用。

### 示例：用 SQLite 保存笔记

额外安装 `pip install sqlmodel`。下面的示例会在运行目录创建 `notes.db`，建表放在应用启动的 `lifespan` 中：

```python
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

engine = create_engine(
    "sqlite:///notes.db", connect_args={"check_same_thread": False}
)


class NoteCreate(SQLModel):
    title: str = Field(min_length=1, max_length=100)


class Note(NoteCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)


class NotePublic(NoteCreate):
    id: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


@app.post("/notes", response_model=NotePublic, status_code=201)
def create_note(note: NoteCreate, session: Annotated[Session, Depends(get_session)]):
    record = Note.model_validate(note)
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


@app.get("/notes", response_model=list[NotePublic])
def list_notes(session: Annotated[Session, Depends(get_session)]):
    return session.exec(select(Note)).all()
```

发送 `POST /notes`，请求体为 `{"title": "学习 FastAPI"}`，返回带有数据库生成 ID 的笔记；再访问 `GET /notes` 可以读取已保存的数据。这里使用自动建表便于入门，正式项目的表结构变更通常交给迁移工具管理。

## 文件上传 / 下载

文件上传和下载是接口的“快递通道”：客户端把图片、文档交给服务器，服务器也可以把报告、附件发送回来。它们使用 HTTP 传输，但数据格式和普通 JSON 请求不同。

### 核心知识点

* 上传通常使用 `multipart/form-data`，需要安装 `python-multipart`。
* `UploadFile` 提供文件名、内容类型和文件读写方法；`list[UploadFile]` 可以接收多个文件。
* 大文件可以分块读取，避免一次把全部内容加载到内存；读取后及时关闭文件。
* `FileResponse` 返回已有文件，`StreamingResponse` 用于逐块输出内容。

### 示例：统计上传大小并下载文本

如未安装上传依赖，先执行 `pip install python-multipart`。

```python
from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse

app = FastAPI()


@app.post("/upload")
async def upload_file(file: UploadFile):
    size = 0
    try:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
        return {"filename": file.filename, "size": size}
    finally:
        await file.close()


@app.get("/download")
def download_file():
    content = "这是一个 FastAPI 下载示例。\n".encode("utf-8")
    return StreamingResponse(
        iter([content]),
        media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="example.txt"'},
    )
```

在 `/docs` 的 `POST /upload` 中选择文件，可得到文件名和字节数；访问 `GET /download` 会下载 `example.txt`。上传接口只统计大小，不保存文件。

## 跨域处理

跨域处理像给前端配置“通行名单”：浏览器页面与 API 的来源不同，浏览器就会检查服务器是否允许这个页面读取响应。前后端分别运行在 `localhost:5173` 和 `localhost:8000` 时，就属于跨域访问。

### 核心知识点

* 来源由协议、主机和端口共同决定，任一项不同就不是同源。
* 使用 `CORSMiddleware` 配置允许的来源、请求方法、请求头。
* 浏览器可能先发送 `OPTIONS` 预检请求，中间件会处理这类跨域检查。
* 携带 Cookie 等凭证时，需要设置 `allow_credentials=True`，并明确列出允许的来源、方法和请求头。
* CORS 是浏览器的访问规则，不替代服务端认证和权限控制。

### 示例：允许本地前端读取接口

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/hello")
def hello():
    return {"message": "你好，前端"}
```

在来源为 `http://localhost:5173` 的前端页面中调用 `fetch("http://localhost:8000/hello")`，浏览器就可以读取响应。`http://127.0.0.1:5173` 是另一个来源，需要单独加入名单。

## 后台任务

后台任务像“先给回执，再做后续工作”：接口先告诉客户端请求已接收，再执行日志写入、通知等不影响当前响应的操作，让用户不必一直等待。异步编程的基本原理见前面的“异步处理”，这里侧重响应发出后的任务执行。

### 核心知识点

* 在接口参数中声明 `BackgroundTasks`，FastAPI 会自动提供任务容器。
* `add_task(函数, 参数...)` 登记任务，响应发送后执行；不要在登记时直接调用函数。
* 任务可以是同步或异步函数，但仍在应用进程中运行，不是独立任务队列。
* 适合轻量任务；需要持久化、重试或大量计算时，应使用独立任务队列。

### 示例：响应后记录访问日志

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_log(item_id: int):
    with open("visits.log", "a", encoding="utf-8") as file:
        file.write(f"访问商品：{item_id}\n")


@app.post("/items/{item_id}/visit", status_code=202)
def record_visit(item_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, item_id)
    return {"message": "已接收访问记录"}
```

发送 `POST /items/5/visit`，先收到 `202` 响应，随后运行目录的 `visits.log` 追加一条记录。响应成功表示任务已登记，不代表写入已经完成。

## 部署上线

部署上线是把本机程序变成“持续对外服务的窗口”：除了启动代码，还要考虑监听地址、进程数量、HTTPS 和故障重启，让其他人能够稳定访问接口。

### 核心知识点

* Uvicorn 是运行 FastAPI 应用的 ASGI 服务器，`main:app` 指定模块和应用对象。
* `--reload` 用于开发时自动重载，生产运行时关闭；它不能与多 worker 模式一起使用。
* `--host 0.0.0.0` 监听所有网络接口，但外部能否访问还取决于网络和防火墙配置。
* `--workers` 启动多个进程，每个进程独立使用内存，内存变量不会自动共享。
* Linux 环境也可以通过 Gunicorn 配合兼容的 Uvicorn worker 管理进程；入门示例直接使用 Uvicorn。
* 生产环境还需通过反向代理或平台配置 HTTPS、自动重启和日志；Docker 可以封装运行环境。

### 示例：用多个进程启动服务

保存以下代码为 `main.py`：

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}
```

在文件所在目录执行：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
```

本机访问 `http://127.0.0.1:8000/health` 应返回 `{"status": "ok"}`；其他设备需要使用服务器实际 IP。这个示例完成服务启动，公开上线时还需完成 HTTPS 等环境配置。



# 参考

[菜鸟教程](https://www.runoob.com/fastapi/fastapi-tutorial.html)  
[FastAPI从入门到精通](https://blog.csdn.net/inuex/article/details/159203950)
