## Faiss的简介

如果你正在构建一个 RAG 系统、智能问答平台、文本相似度比对、或者 AI 搜索系统，你几乎一定听过 FAISS 这个名字。

FAISS（Facebook AI Similarity Search） 是由 Meta（原 Facebook）开发的开源向量检索引擎，专为“海量向量的高效相似度搜索”而设计。它又不是数据库，而是一个超高性能的 C++/Python 向量索引库，可以让你在本地环境下进行数百万级别的向量匹配操作。如果你要的是嵌入项目的轻量向量库，首选 FAISS。

## 应用场景
* 语义检索：根据问句的语义找到最接近的文档片段
* RAG 系统：作为大模型上下文召回的向量库
* 文本聚类：找出相似内容或主题群组
* 图像 / 视频搜索：嵌入图像特征后进行相似内容比对

## 特点
特点|	优势说明
---|---
性能极强	|支持百万向量以内毫秒级响应（本地 CPU / GPU）
部署轻量|	不需要服务器，不需要 Docker，一句 pip 即可
本地私有化友好|	所有数据都在你机器上，无外泄风险
模块组合灵活	|提供 10 多种索引结构，适配不同精度 / 速度场景

## 如何衡量“相似”
向量检索的本质是：你给我一个向量，我从海量向量中找到它的“邻居”们。

常见的相似度度量方式有两种：

1. 欧氏距离（L2 距离）
衡量两个向量在空间中的“直线距离”，距离越近表示越相似。

```
D(x, y) = √[(x1 - y1)^2 + (x2 - y2)^2 + ... + (xn - yn)^2]
```

FAISS 中使用索引类型：IndexFlatL2。

2. 余弦相似度（Cosine Similarity）
衡量两个向量之间的夹角，夹角越小相似度越高，值越接近 1 表示越相似。
```
cos(θ) = (x · y) / (||x|| × ||y||)
```

其中：

* x · y 表示两个向量的点积   
* ||x|| 是向量的 L2 范数（模长）      

FAISS 中使用：IndexFlatIP + 向量归一化。


## FAISS 在 RAG 系统中的角色
在现代 RAG（检索增强生成）系统中，FAISS 扮演着 **“语义中间人”** 的角色：帮大模型找出最有可能相关的上下文。

 标准 RAG 工作流图：
 ```
 【用户问题】
     ↓
【句子向量化】
     ↓
【FAISS 向量检索】
     ↓
【相关文段 TopK】
     ↓
【Prompt 拼接】
     ↓
【大模型生成回答】
 ```
**为什么大模型必须搭配向量检索？**    
* 大模型不能 **“凭空知道”你给的知识**；   
* 文档直接塞进 prompt 会超长、杂乱、失真；   
* FAISS 帮你精准提取与问题最相关的语义片段，极大提升准确率。

**Prompt 构建建议（适用于 LLM）**   
推荐使用 **“资料块 + 问题”** 结构拼接 prompt，提升上下文可读性：
```
你是一位专业的知识助手，请根据以下资料回答用户的问题。

[1] 公司是法人，有独立资产。
[2] 股东以其出资额为限承担责任。

问题：公司和股东的法律责任分别是什么？
```


**Prompt 拼接函数示例：**   
```
def build_prompt(query: str, matched_chunks: list) -> str:
    context_block = "\n".join([f"[{i+1}] {c}" for i, c in enumerate(matched_chunks)])
    return f"""你是一位专业的法律助手，请根据以下资料回答用户的问题。
{context_block}

问题：{query}
"""
```
**构建 prompt 时的实用技巧：**  

项目	|建议
---|---
上下文数量|	通常建议 Top 3～5 段，超过影响 token 上限
加编号	|[1]、[2]…便于 LLM 回答引用
指令句	|如果找不到答案，请说不知道，减少幻觉输出
合并片段	|同类文段可合并为一条，节省空间

## 简单流程
 
1、安装   
以cpu版本为例  
```
pip install faiss-cpu
```
2、 文本准备（示例为法律文档）    
创建一个简单的样本文本，内容如下（law.txt）：
```
第七条：公司是企业法人，有独立的法人财产。
第八条：公司以其全部财产对公司债务承担责任。
董事会对公司的经营决策具有最终权力。
股东大会是公司的最高权力机构。
```
3、文本切片 + 嵌入向量生成
```
from sentence_transformers import SentenceTransformer
import numpy as np

# 加载文档内容（每行为一个 chunk）
with open("law.txt", "r", encoding="utf-8") as f:
    docs = [line.strip() for line in f if line.strip()]

# 加载 embedding 模型（可替换为 bge/text2vec）
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 生成向量（默认维度 384）
embeddings = model.encode(docs, normalize_embeddings=True)
print(f"共生成 {len(embeddings)} 个向量，每个维度为 {embeddings.shape[1]}")
```
4、构建 FAISS 索引
```
import faiss

# 创建 IndexFlatIP（使用 Cosine 相似度需先归一化）
dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(embeddings)
```
5、输入问句并向量化
```
query = "公司法人要承担哪些责任？"
query_vec = model.encode([query], normalize_embeddings=True)
```
6、使用 FAISS 执行搜索
```
# 查询最相似的 top-k 向量
k = 2
D, I = index.search(np.array(query_vec), k)

# 输出检索结果
for rank, idx in enumerate(I[0]):
    print(f"[Top {rank+1}] {docs[idx]}")
```
输出:
```
[Top 1] 公司以其全部财产对公司债务承担责任。
[Top 2] 公司是企业法人，有独立的法人财产。
```
## 结合大模型实例
1、定义工具
```
import os
from langchain_community.tools.tavily_search import TavilySearchResults

# 定义 AVILY_KEY 密钥
os.environ["TAVILY_API_KEY"] = "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"
# 查询 Tavily 搜索 API
search = TavilySearchResults(max_results=1)
```
2、定义Retriever
```
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import dotenv
dotenv.load_dotenv()

# 1. 提供一个大模型
os.environ['OPENAI_API_KEY'] = os.getenv("aliyun_api_key")
os.environ['OPENAI_BASE_URL'] = os.getenv("aliyun_base_url")


embedding_model = OpenAIEmbeddings(model="qwen3-vl-embedding")

# 2.加载HTML内容为一个文档对象
loader = WebBaseLoader("https://zh.wikipedia.org/wiki/%E7%8C%AB")
docs = loader.load()
#print(docs)

# 3.分割文档
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

documents = splitter.split_documents(docs)

# 4.向量化 得到向量数据库对象
vector = FAISS.from_documents(documents, embedding_model)

# 5.创建检索器
retriever = vector.as_retriever()

# 测试检索结果
# print(retriever.invoke("猫的特征")[0])
```
3、创建工具、工具集
```
from langchain.tools.retriever import create_retriever_tool

# 创建一个工具来检索文档
retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="wiki_search",
    description="搜索维基百科",
)

# 构建工具集
tools = [search, retriever_tool]
```
4、语言模型调用工具
```
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 获取大模型
model = ChatOpenAI(model="qwen3-max")

# 模型绑定工具
model_with_tools = model.bind_tools(tools)

# 根据输入自动调用工具
# messages = [HumanMessage(content="今天上海天气怎么样")]
# response = model_with_tools.invoke(messages)
# print(f"ContentString: {response.content}")
# print(f"ToolCalls: {response.tool_calls}")
```
5、创建Agent程序
```
from langchain import hub
prompt = hub.pull("hwchase17/openai-functions-agent")

# print(prompt.messages)
```
```
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

# 创建Agent对象
agent = create_tool_calling_agent(model, tools, prompt)

# 创建AgentExecutor对象
agent_executor = AgentExecutor(agent=agent, tools=tools,verbose=True)
```
6、运行Agent
```
print(agent_executor.invoke({"input": "猫的特征"}))
```

7、添加记忆
```
from langchain_community.chat_message_histories import ChatMessageHistory

from langchain_core.chat_history import BaseChatMessageHistory

from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

# 调取指定session_id对应的memory
def get_session_history(session_id: str) -> BaseChatMessageHistory:

    if session_id not in store:
        store[session_id] = ChatMessageHistory()

    return store[session_id]

agent_with_chat_history = RunnableWithMessageHistory(
    runnable=agent_executor,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

response = agent_with_chat_history.invoke(
    {"input": "Hi，我的名字是Cyber"},
    config={"configurable": {"session_id": "123"}},
)

print(response)
```
输出：
```
> Entering new AgentExecutor chain...
你好，Cyber！很高兴见到你。有什么我可以帮助你的吗？

> Finished chain.
{'input': 'Hi，我的名字是Cyber', 'chat_history': [], 'output': '你好，Cyber！很高兴见到你。有什么我可以帮助你的吗？'}
```
继续提问：
```
response = agent_with_chat_history.invoke(
    {"input": "我叫什么名字?"},
    config={"configurable": {"session_id": "123"}},
)

print(response)
```
输出：
```
Entering new AgentExecutor chain...
你叫Cyber。有什么特别的事情想和我分享吗？

> Finished chain.
{'input': '我叫什么名字?', 'chat_history': [HumanMessage(content='Hi，我的名字是Cyber', additional_kwargs={}, response_metadata={}), AIMessage(content='你好，Cyber！很高兴见到你。有什么我可以帮助你的吗？', additional_kwargs={}, response_metadata={})], 'output': '你叫Cyber。有什么特别的事情想和我分享吗？'}
```
**如果修改其他session_id，则这段记忆就不知道，实现不同id对应不同的记忆。**


原文链接：[https://blog.csdn.net/sinat_28461591/article/details/147031798](https://blog.csdn.net/sinat_28461591/article/details/147031798)
SentenceTransformers 库介绍: [https://zhuanlan.zhihu.com/p/457876366](https://zhuanlan.zhihu.com/p/457876366)