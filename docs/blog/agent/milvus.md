# Milvus向量数据库
## 介绍
在 AI 技术爆发的今天，大模型（LLM）已成为智能应用的核心引擎。然而，单纯的预训练模型存在知识滞后、幻觉问题、私有数据无法接入等致命缺陷。如何让 AI 拥有"长期记忆"和"私有知识库"？答案就是——向量数据库。

Milvus 作为全球领先的开源 向量数据库，已被 Salesforce、PayPal、Shopee、Airbnb 等 5000+ 企业采用，在 GitHub 上获得超过 30,000+ Stars，成为 AI 应用的基础设施标配。从 RAG（检索增强生成）到以图搜图，从个性化推荐到智能问答，Milvus 正在重塑我们构建 AI 应用的方式。

## 主要特点
特性	|说明
---|---
高性能	|支持十亿级向量的毫秒级检索，GPU 加速
云原生架构	|存算分离设计，支持水平扩展（Kubernetes 部署）
多索引类型	|支持 IVF、HNSW、DiskANN 等多种 ANN 索引算法
混合搜索	|支持向量搜索 + 标量过滤（metadata filtering）
多语言 SDK	|提供 Python、Java、Go、Node.js 等客户端
生态丰富	|与 LangChain、LlamaIndex、Spark 等无缝集成


**高性能**:官方说其性能是其他向量数据库（Vector Database）的2-5倍
## 应用场景
* RAG（检索增强生成）：为大语言模型提供外部知识库检索
* 以图搜图 / 以文搜图：电商商品搜索、版权图片检测
* 语义搜索：文档、代码、问答系统的智能检索
* 推荐系统：基于用户/物品向量相似度的个性化推荐
* 生物信息学：蛋白质序列、基因序列相似性分析
* 对话机器人
* 声纹识别
## 向量数据库对比
### 与关系数据库区别
首先先说一下向量数据库与传统关系数据库的不同，如你做了一个AI日记本应用，你想知道哪几天你的心情比较好。如果想知道如果你把日记存在 MySQL 里，你会怎么查？SELECT * FROM diary WHERE content LIKE '%开心%'？这种关键词匹配根本不靠谱。用户可能写的是"今天很愉快"、"心情不错"、"感觉很棒"，这些表达心情好的方式千变万化，关键词匹配会漏掉大量结果。
**这就是传统关系型数据库在 AI 应用中的根本局限：它只能做精确匹配和关键词匹配，无法理解语义。** **而向量数据库的本质就是：把文本转换成高维向量，通过向量之间的距离来衡量语义相似度。**
>传统数据库（MySQL、PostgreSQL）：   
  → 精确匹配（SELECT * FROM users WHERE id = 123）   
  → 结构化数据（数字、字符串、日期）   
  → 索引：B-Tree、Hash       
向量数据库（Milvus）：
  → 相似度匹配（找"语义最相似"的内容）   
  → 非结构化数据（文本、图像、音频）  
  → 索引：IVF、HNSW、DiskANN   

### 不同向量数据库对比
* Faiss: 高性能计算引擎，适用于纯向量计算加速，但需要搭配存储系统。
* Milvus: 全功能向量数据库，适用于大规模生产环境，支持GPU加速，操作简单。
* Elasticsearch(ES): 性能强大，功能复杂。
* ChromaDB:开发友好，适用于轻量级应用和快速迭代。
* Pinecone:闭源。
### Milvus版本
* **Lite:** 精简版(开发版)。
* Standalone:单机版。
* **Distributed:** 分布式版本。

**推荐Lite和Distributed版** ，单机版功能比较完全但只放在一台机器上工作，不利于企业容灾。

**Milvus Lite 目前支持以下环境：**
* Ubuntu >= 20.04（x86_64 和 arm64）   
* MacOS >= 11.0（苹果硅 M1/M2 和 x86_64）

**参考文章**中有基于Docker Desktop和Windows的Milvus本地部署教程。 







## 参考文章
官方文档：[https://milvus.io/docs/zh](https://milvus.io/docs/zh)   
PyMilvus官方API文档：[https://milvus.io/api-reference/pymilvus/v2.4.x/About.md](https://milvus.io/api-reference/pymilvus/v2.4.x/About.md)    
人话版参考：[https://zhuanlan.zhihu.com/p/1912478457285293545](https://zhuanlan.zhihu.com/p/1912478457285293545)    
docker部署milvus：[https://blog.csdn.net/m0_62102955/article/details/151868248](https://blog.csdn.net/m0_62102955/article/details/151868248)