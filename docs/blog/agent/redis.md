# Redis
## 简介
Redis 是一个使用 ANSI C 编写的、开源的、基于内存的键值存储系统。它支持网络连接，并提供了多种语言的 API。虽然常被用作缓存，但其能力远不止于此。它可以作为：

* 数据库：持久化存储结构化数据。

* 缓存：为后端数据库提供毫秒级响应的读取层。

* 消息中间件：通过发布/订阅模式实现应用解耦。

核心特点：

* 极致性能：数据存储在内存中，读写速度极快，官方基准测试可达10万+ QPS。

* 丰富数据结构：原生支持字符串（String）、哈希（Hash）、列表（List）、集合（Set）、有序集合（Sorted Set）等，还支持位图（Bitmap）、HyperLogLog、地理空间（Geo）等高级数据类型。

* 持久化能力：提供 RDB（快照）和 AOF（追加日志）两种持久化机制，确保数据安全。

* 高可用与可扩展：通过主从复制、哨兵（Sentinel）模式和原生集群（Cluster）模式，轻松构建高可用、可水平扩展的分布式系统。

* 原子性操作：所有单个命令都是原子性的，并支持事务（MULTI/EXEC）和 Lua 脚本，以保证复杂操作的原子性

##  Redis 应用领域
Web后端：会话存储、页面缓存、API响应缓存

实时分析：排行榜、计数器、实时仪表盘

消息队列：任务队列、事件驱动架构

AI/ML：RAG（检索增强生成）的向量数据库、特征存储

游戏：玩家状态、实时排行榜、社交关系

物联网：设备状态、实时数据流处理

金融：交易限流、欺诈检测、实时风控

## Redis在RAG中的使用
什么是检索增强生成（RAG）？  
大型语言模型 (LLM) 生成类似人类的文本，但受其训练数据的限制。**RAG 通过将其与存储在 Redis 向量数据库中的外部领域特定数据集成来增强 LLM。**

RAG 包括三个主要步骤

* 检索：使用向量搜索和基于用户查询的过滤器从 Redis 中获取相关信息。
* 增强：为 LLM 创建提示，包括用户查询、相关上下文和附加指令。
* 生成：将 LLM 生成的响应返回给用户。

RAG 使 LLM 能够使用实时信息，提高生成内容的准确性和相关性。Redis 因其速度、多功能性和易用性而成为 RAG 的理想选择。

**Redis 在 RAG 中的作用：**

Redis 为管理实时数据提供了一个强大的平台。它支持向量的存储和检索，这对于处理大规模、非结构化数据和执行相似性搜索至关重要。Redis 使其适用于 RAG 的主要特性和组件包括

* 向量数据库：存储和索引语义表示非结构化数据的向量嵌入。
* 语义缓存：在 RAG 流水线中缓存常见问题 (FAQ)。使用向量搜索，Redis 检索先前回答的类似问题，降低 LLM 推理成本和延迟。
* LLM 会话管理器：存储 LLM 和用户之间的对话历史记录。Redis 获取聊天历史记录中最近且相关的部分以提供上下文，从而提高响应的质量和准确性。
* 高性能和可扩展性：Redis 以其低延迟和高吞吐量而闻名，是需要快速数据检索和生成的 RAG 系统和 AI 代理的理想选择。

**使用 Redis 构建 RAG 应用：**

要使用 Redis 构建 RAG 应用，请遵循以下一般步骤

* 设置 Redis：首先设置一个 Redis 实例并将其配置为处理向量数据。

* 使用框架:

  * Redis 向量库 (RedisVL)：RedisVL 通过高效管理向量和元数据来增强生成式 AI 应用的开发。它允许存储向量嵌入并促进快速相似性搜索，这对于在 RAG 中检索相关信息至关重要。
  * 流行的 AI 框架：Redis 与各种 AI 框架和工具无缝集成。例如，将 Redis 与用于构建语言模型的库 LangChain 或 LlamaIndex 结合使用，使开发人员能够创建复杂的 RAG 流水线。这些集成支持高效的数据管理和构建实时 LLM 链。
  * Spring AI 和 Redis：使用带有 Redis 的 Spring AI 简化了 RAG 应用的构建。Spring AI 提供了一种结构化的方法来将 AI 功能集成到应用中，而 Redis 处理数据管理，确保 RAG 流水线高效且可扩展。
* 嵌入并存储数据：使用合适的模型（例如 BERT、GPT）将数据转换为向量嵌入。将这些嵌入存储在 Redis 中，在那里可以基于向量搜索快速检索它们。

* 与生成模型集成：使用可以利用检索到的数据的生成式 AI 模型。该模型将使用存储在 Redis 中的向量来增强其生成过程，确保输出信息相关且最新。

* 查询和生成：实现查询逻辑，根据输入提示从 Redis 中检索相关向量。将这些向量输入生成模型以产生增强的输出。

**使用 Redis 进行 RAG 的优势：**
* 效率：Redis 的内存数据存储确保检索操作以最小的延迟执行。
* 可扩展性：Redis 可以横向扩展，无缝处理不断增长的数据量和查询。
* 灵活性：Redis 支持各种数据结构并与 AI 框架集成。

总而言之，Redis 为实现 RAG 提供了一个强大且高效的平台。其向量管理功能、高性能以及与 AI 框架的无缝集成使其成为利用实时数据检索增强生成式 AI 应用的理想选择。

## 用Redis构建RAG应用代码
**1.搭建并配置 Redis 环境**

首先需要一个 Redis 实例，推荐用支持向量搜索的版本（比如 Redis 6.2+）。安装后，通过配置文件开启向量索引支持，确保能存储和检索向量嵌入。如果是云环境，也可以直接用 Redis Cloud，省去本地部署的麻烦。[Redis Cloud官方网站](https://cloud.redis.io/#/login)

**2.选择合适的开发框架**

单独操作 Redis 可能有点繁琐，借助框架能事半功倍：

* RedisVL：Redis 官方的 Python 库，专门优化了向量和元数据管理，支持快速构建向量索引、执行相似性搜索，还集成了 CLI 工具，调试起来很方便。
* 主流 AI 框架：Redis 能和 LangChain、LlamaIndex 等无缝集成。比如用 LangChain 时，只需几行代码就能把 Redis 设为向量存储，再搭配 LLMs（如 GPT-3.5）构建完整的 RAG 管道，快速实现 “检索→增强→生成” 的全流程。

**3.嵌入数据并存储到 Redis**

把需要用到的外部数据（如文档、知识库）转换成向量嵌入：

* 先用嵌入模型（如 Sentence-BERT）把文本转换成向量（比如每个文本转成 768 维向量）；
* 用 RedisVL 或 LangChain 的 API，将向量和对应的元数据（如文本内容、来源）一起存储到 Redis 中，并创建向量索引（指定距离度量方式，如余弦相似度）。

**4.集成生成式模型**

选择一个合适的 LLM（如 GPT-4、Llama 2 等），通过 API 或本地部署的方式集成到系统中。关键是要让 LLM 能接收 “用户查询 + 检索到的上下文” 作为输入，比如构造这样的提示：“基于以下上下文回答用户问题：{检索到的文档内容}\n 用户问题：{user_query}”。

**5.实现查询与生成逻辑**

当用户输入查询时，系统会：

* 用同样的嵌入模型把查询转换成向量；
* 调用 Redis 的向量搜索，根据相似度从索引中找到 Top N 相关文档；
* 把这些文档内容和用户查询整合成提示，传给 LLM；
* 接收 LLM 的回复，返回给用户。

**示例代码：**   
这里直接用 Redis Cloud云环境，不用本地部署。但注意连接方式，可以参考[带你入门免费的Redis Cloud](https://www.joinquant.com/community/post/detailMobile?postId=44286)。还有几个注意的点：
*  redisvl 在 load() 时，通常需要的是：字符串、数字、bytes或者它能自动处理的向量格式，有时候embedding返回的是 Python 的 list，就会报错。可以把向量转成字节数组，embedding = np.array(vectorizer.embed(doc), dtype=np.float32).tobytes()
* 有时候连接的方式/端口/服务端协议不匹配也会报错，比如你设置了ssl=True，而Redis Cloud 需要 TLS，你用了错误的连接方式。

**关于第二点，我在应用时踩过坑，你只需要检查**  
1）确认这个端口是不是 TLS 端口
Redis Cloud 通常会给你两种连接信息：

* 普通 TCP 端口
* TLS/SSL 端口

如果你拿的是普通端口，就不能加： ssl=True。

如果是 TLS 端口，必须加：ssl=True

2）确认你是不是应该用 rediss://

比如我开始使用的是
>index.connect("redis://default:password@host:port")

如果是 SSL/TLS，应该改成：

>index.connect("rediss://default:密码@host:port")

注意是：

redis:// = 非 SSL  
rediss:// = SSL/TLS

这个可以在Redis CLI中确认。

```
import redis
import os
import numpy as np
from openai import OpenAI
from redisvl.index import SearchIndex
from redisvl.query import VectorQuery
from redisvl.utils.vectorize import HFTextVectorizer
import dotenv

dotenv.load_dotenv()

# =========================
# 1. 连接 Redis Cloud
# =========================
r = redis.Redis(
    host="redis-19613.c256.us-east-1-2.ec2.cloud.redislabs.com",
    port=19613,
    username="default",
    password="......",
    decode_responses=True,
)


# 测试连接
print("PING:", r.ping())

# =========================
# 2. 向量化模型
# =========================
vectorizer = HFTextVectorizer(model="sentence-transformers/all-MiniLM-L6-v2")
vector_dims = vectorizer.dims

# =========================
# 3. 创建 RedisVL 索引
# =========================
schema = {
    "index": {
        "name": "rag_demo_index",
        "prefix": "doc"
    },
    "fields": [
        {"name": "text", "type": "text"},
        {
            "name": "text_embedding",
            "type": "vector",
            "attrs": {
                "dims": vector_dims,
                "distance_metric": "cosine",
                "algorithm": "hnsw",
                "datatype": "float32"
            }
        }
    ]
}

index = SearchIndex.from_dict(schema)
index.set_client(r)
index.create(overwrite=True)

# =========================
# 4. 写入数据到 Redis
# =========================
documents = [
    "Redis 是一个开源的内存数据存储，用作数据库、缓存、流引擎和消息代理。",
    "检索增强生成（RAG）是一种技术，它将神经网络语言模型与外部知识检索系统结合起来。",
    "RedisVL 是一个专门为 AI 和 LLM 应用程序设计的 Redis 向量数据库客户端库。"
]

data = []
for i, doc in enumerate(documents, start=1):
    embedding = np.array(vectorizer.embed(doc), dtype=np.float32).tobytes()
    data.append({
        "id": f"doc:{i}",
        "text": doc,
        "text_embedding": embedding
    })

index.load(data)
print("数据已写入 Redis Cloud")

# =========================
# 5. 从 Redis 读取测试
# =========================
print("当前 Redis keys：", r.keys("*"))


# ==========================================
# 向量检索 (Retrieval)
# ==========================================
query_text = "请问什么是 RedisVL？"
print(f"\n用户提问: '{query_text}'")

# 对用户的查询也进行向量化
query_embedding = vectorizer.embed(query_text)

# 构建向量搜索查询，检索最相关的 2 条文档
query = VectorQuery(
    vector=query_embedding,
    vector_field_name="text_embedding",
    return_fields=["text"],
    num_results=2
)

# 执行查询
results = index.query(query)
retrieved_texts = [result["text"] for result in results]

context = "\n".join(retrieved_texts)
print("\n[检索到的上下文]:")
print(context)

# ==========================================
# 大模型生成回答 (Generation)
# ==========================================
# 此处以 OpenAI 为例。如果是本地大模型可以使用 ollama 或 vLLM。
# 请确保你的环境变量中设置了 OPENAI_API_KEY
print("\n[LLM 最终回答]:")


client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("aliyun_api_key"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 结合上下文构造提示词
prompt = f"请利用以下上下文信息来回答用户的问题。\n\n上下文:\n{context}\n\n用户问题: {query_text}\n回答:"

response = client.chat.completions.create(
    model="qwen3-max", 
    messages=[
        {"role": "system", "content": "你是一个有用的、专业的 AI 助理。"},
        {"role": "user", "content": prompt}
    ]
)

print(response.choices[0].message.content)
```

输出：
```
数据已写入 Redis Cloud
当前 Redis keys： ['doc:01KPZSJDBRQ8AT5TC8P0FW6Q25', 'doc:01KPZSJDBRQ8AT5TC8P0FW6Q24', 'doc:01KPZT0633GR69ND5F9AXQZEGZ', 'doc:01KPZSNJ7MM4K96S37WNYDP393', 'doc:01KPZSNJ7MM4K96S37WNYDP392', 'doc:01KPZT0633GR69ND5F9AXQZEH0', 'doc:01KPZSNJ7MM4K96S37WNYDP391', 'doc:01KPZT0633GR69ND5F9AXQZEGY', 'doc:01KPZSJDBRQ8AT5TC8P0FW6Q23']

用户提问: '请问什么是 RedisVL？'

[检索到的上下文]:
RedisVL 是一个专门为 AI 和 LLM 应用程序设计的 Redis 向量数据库客户端库。
RedisVL 是一个专门为 AI 和 LLM 应用程序设计的 Redis 向量数据库客户端库。

[LLM 最终回答]:
RedisVL 是一个专门为 AI 和大语言模型（LLM）应用程序设计的 Redis 向量数据库客户端库。它简化了在 Redis 中存储、索引和检索向量数据的过程，帮助开发者高效构建基于向量搜索的 AI 应用。
```


## Redis的数据是存在内存中的，它和传统内存存储区别
Redis 作为内存数据库，数据默认存储在内存中，断电或服务重启会导致数据丢失。为了解决这个问题，Redis 提供了两种核心的持久化机制：**RDB（快照） 和 AOF（日志）**。

你可以用一句话概括它们的区别：
* RDB 就像是给数据“拍照片”（记录某个时间点的数据状态）。
* AOF 就像是“记流水账”（记录每一次修改数据的操作）。

**1.RDB (Redis Database) —— 快照模式**

RDB 是 Redis 默认的持久化方式。它的核心思想是在指定的时间间隔内，将内存中的数据集快照写入磁盘，生成一个二进制文件（通常命名为 dump.rdb）。
核心原理
* 触发机制：可以通过配置自动触发（如 save 900 1，表示 900 秒内至少有 1 个键变化就触发），也可以手动执行 SAVE 或 BGSAVE 命令。
* 后台执行与写时复制 (COW)：为了不阻塞主线程，Redis 通常使用 BGSAVE。它会 fork 一个子进程，利用操作系统的写时复制（Copy-On-Write）技术，让子进程在后台将内存数据写入临时文件，最后原子替换旧的 RDB 文件。这意味着在快照生成期间，主进程依然可以处理客户端请求。

优缺点分析

维度|	优势|	劣势
---|---|---
性能	|对性能影响极小，主进程只负责 fork 子进程，不进行磁盘 I/O。	|在数据量极大时，fork 操作可能导致主进程短暂阻塞（毫秒级）。
恢复速度	|极快。加载二进制文件直接还原内存，无需解析命令。	|无。
数据完整性|	文件紧凑，适合备份和灾难恢复。|	会丢失数据。只能恢复到上一次快照的时间点，两次快照之间的数据会丢失。
文件体积|	文件体积小，经过压缩，适合传输。	|无。

**2.AOF (Append Only File) —— 日志模式**

AOF 的核心思想是将 Redis 执行的每一条写命令（如 SET、INCR）以文本协议的形式追加到日志文件末尾（通常命名为 appendonly.aof）。重启时，通过重新执行这些命令来恢复数据。
核心原理
* 写后日志：Redis 先执行命令，再将命令追加到 AOF 缓冲区，最后根据策略刷入磁盘。
* 刷盘策略 (appendfsync)：
  * always：每条命令都立即同步到磁盘。最安全（几乎不丢数据），但性能最差。
  * everysec（推荐）：每秒同步一次。兼顾了性能和安全，最多丢失 1 秒数据。
  * no：由操作系统决定何时同步。性能最好，但数据最不安全。
* AOF 重写 (Rewrite)：随着时间推移，AOF 文件会越来越大（例如对同一个键执行了 100 次 INCR）。Redis 会在后台启动子进程，根据当前内存数据的最新状态，生成一个精简的新 AOF 文件（上述 100 次操作会被合并为一条命令），替换旧文件。

优缺点分析

维度	|优势	|劣势
---|---|---
数据完整性	|极高。配合 everysec 策略，最多只丢 1 秒数据；配合 always 可做到不丢。|	无。
可读性|	文件是文本格式，可读性强，甚至可以手动修改修复。	|无。
恢复速度	|较慢。需要逐条重放命令，数据量大时恢复慢。|	无。
文件体积	|文件体积通常比 RDB 大。	|即使有重写机制，文件依然较大，占用更多磁盘 I/O。

**3.总结与最佳实践**
在实际生产环境中，我们通常不会二选一，而是根据需求组合使用。

RDB vs AOF 对比

特性|	RDB (快照)|	AOF (日志)
---|---|---
记录方式	|全量数据快照（二进制）	|增量操作日志（文本协议）
数据安全性|	低（可能丢失几分钟数据）	|高（最多丢失 1 秒）
恢复速度|	快	|慢
适用场景|	冷备、灾难恢复、主从同步|	核心业务数据、高可靠性要求

💡 推荐方案：混合持久化 (Redis 4.0+)
为了兼顾 RDB 的快速恢复 和 AOF 的数据安全，Redis 4.0 引入了混合持久化。
* 原理：在进行 AOF 重写时，不是生成纯文本的 AOF 文件，而是将当前内存数据以 RDB 二进制格式 写入文件前半部分，将重写期间产生的增量命令以 AOF 文本格式 追加到文件后半部分。
* 优势：
恢复快：加载前半部分的 RDB 数据非常快。
数据全：后半部分的 AOF 日志保证了最后一次快照后的数据不丢失。
配置简单：只需在配置文件中开启 aof-use-rdb-preamble yes。

生产环境建议：   
同时开启 RDB 和 AOF，并使用混合持久化模式，AOF 刷盘策略设为 everysec。这样既能保证数据尽可能不丢失，又能确保在故障重启时以最快速度恢复服务。

（everysec 策略的核心机制是：每秒将缓冲区中的数据同步到磁盘一次。
具体来说，当 Redis 执行写操作时，会先将命令写入内存中的 AOF 缓冲区。然后，一个后台线程会每隔一秒钟调用一次操作系统的 fsync 函数，将这个缓冲区里的所有数据真正写入到磁盘的 AOF 文件中。
everysec 是在性能和数据安全性之间做出的一个折中方案，也是 Redis 官方推荐的默认配置。）




## 参考

[快速入门：使用 Redis 进行 RAG](https://redis.ac.cn/docs/latest/develop/get-started/rag/)

https://cloud.tencent.com/developer/article/2653346

一文搞懂redis的所有知识点：https://zhuanlan.zhihu.com/p/663851226

https://blog.csdn.net/The_Thieves/article/details/149205091

