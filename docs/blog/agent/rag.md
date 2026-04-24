---
title: rag
date: 2026-03-07
authors:
  - name: yyhhao
    email: 1968306533@qq.com
tags:
  - AI
  - RAG
    
draft: false
comments: true
---
# RAG(检索增强生成)
## 简介
**通⽤的基础⼤模型存在一些问题：**    
* LLM的知识不是实时的，模型训练好后不具备自动更新知识的能力，会导致部分信息滞后
* LLM领域知识是缺乏的，大模型的知识来源于训练数据，这些数据主要来自公开的互联网和开源数据集，无法覆盖特定领域或高度专业化的内部知识
* 幻觉问题，LLM有时会在回答中⽣成看似合理但实际上是错误的信息
* 数据安全性

![](image\rag1.png)
RAG（Retrieval-Augmented Generation）即检索增强生成，为大模型提供了从特定数据源检索到的信息，以此来修正和补充生成的答案。可以总结为一个公式：RAG = 检索技术 + LLM 提示

## 工作原理

简单来讲，RAG工作分为两条线：**离线准备线**和**在线服务线**。
![](image\rag2.png)
   
离线准备就是，不停的在后台运行程序，源源不断地从各个来源获取各种信息资料，经过分割处理把它们进行向量化，然后存入向量数据库（企业内部或私有数据库）。       
在线服务就是，用户提问时，并不会直接把问题给模型，而是先从自己的向量数据库抽取相关的匹配资料，然后和用户的提问结合到一起，然后形成我们的提示词优化，最终再去提问模型。相当于模型有更多的参考，使模型在某些不足的领域或者未来的领域，借助我们提供的资料形成回答。

**标准流程图：**
![](image\rag3.png)

RAG 标准流程由索引（Indexing）、检索（Retriever）和生成（Generation）三个核心阶段组成。    
* 索引阶段，通过处理多种来源多种格式的文档提取其中文本，将其切分为标准长度的文本块（chunk），并进行嵌入向量化（embedding），向量存储在向量数据库（vector database）中。
  * 加载文件
  * 内容提取
  * 文本分割 ，形成chunk
  * 文本向量化
  * 存向量数据库
* 检索阶段，用户输入的查询（query）被转化为向量表示，通过相似度匹配从向量数据库中检索出最相关的文本块。
  * query向量化
  * 在文本向量中匹配出与问句向量相似的top_k个
* 生成阶段，检索到的相关文本与原始查询共同构成提示词（Prompt），输入大语言模型（LLM），生成精确且具备上下文关联的回答。
  * 匹配出的文本作为上下文和问题一起添加到prompt中
  * 提交给LLM生成答案

## 总结
模型本质上就是用户输入，模型给出输出，用户能做的就是在输入上做功夫。   
RAG就是在向模型提问之前基于已有的知识库或文档内容做检索，确保向模型提问的内容更精准以及包含足够的信息量用以提供给模型。

RAG的核心价值：
* 解决知识实效性问题：大模型的训练数据有截止时间，RAG 可以接入最新文档（如公司财报、政策文件），让模型输出 “与时俱进”。
* 降低模型幻觉：模型的回答基于检索到的事实性资料，而非纯靠自身记忆，大幅减少编造信息的概率。
* 无需重新训练模型：相比微调（Fine-tuning），RAG 只需更新知识库，成本更低、效率更高。

## 补充：实际RAG系统的评价指标
RAG系统的评价指标涵盖检索、生成、端到端和业务四大维度，通过量化指标评估系统性能和业务价值。

**核心概念：**
RAG系统结合了检索（Retrieval）和生成（Generation）两大模块：**系统首先从知识库中检索相关上下文信息，再利用这些信息生成最终答案。评价RAG系统的核心目标是确保检索到的信息准确且生成内容可靠，同时衡量系统在实际业务中的价值。** 

**检索层指标：**

检索层指标用于衡量系统找到有用信息的能力，主要包括：
* 准确率（Precision）：检索结果中相关文档占比。 
* 召回率（Recall）：系统检索到的相关文档占所有相关文档的比例。 
* F1分数：准确率和召回率的调和平均，用于综合评价。 
* 平均倒数排名（MRR）：衡量第一个相关文档在检索结果中的排名。 
* 归一化折损累积增益（NDCG）：考虑文档相关性等级和排序位置的综合指标。 
* 平均精确率均值（MAP）：对所有查询的平均精确率，反映整体排序效果。 
* 上下文相关性：通过人工或LLM判断检索片段与查询的语义匹配程度。 

我们常看到：精确度@k、召回@k、NDCG@k等，以就NDCG@k为例含义就是：用来衡量排名前k个检索结果的相关性和排序合理性


**生成层指标：**

生成层指标关注模型输出的质量和可靠性：
* 忠实度（Faithfulness）：生成内容是否基于检索到的真实信息。 
* 答案正确性（Answer Correctness）：输出是否符合事实或知识库内容。 
* 回答相关性（Answer Relevance）：答案与用户查询的匹配程度。 


**端到端指标：**

端到端指标综合检索和生成效果，评估系统整体性能：
* 上下文召回率与精确率：衡量系统在整个流程中是否有效利用检索信息。 
* Top-K覆盖率：前K条检索结果中包含相关信息的比例。 

**业务层指标：**

业务层指标关注RAG系统在实际应用中的价值：
* 用户满意度：通过问卷或行为数据评估用户体验。 
* 人工转接率：衡量系统自动回答能力，降低人工干预需求。 
* 鲁棒性与安全性：系统在异常输入或对抗性攻击下的表现。 


**实施建议：**
* 数据驱动评估：使用真实或合成问答数据构建测试集，避免主观判断。 
* 模块拆解：分别评估检索和生成模块，便于定位问题和优化。 
* 闭环优化：通过“评估→优化→再评估”循环持续提升系统性能。 
* 工具选型：可结合LangChain、LlamaIndex等框架快速搭建RAG评估管道。 

通过上述指标体系，开发者可以科学量化RAG系统的性能，从而提升回答准确性、减少幻觉输出，并确保系统在生产环境中创造实际业务价值。

## 补充 RAG中混合检索评估指标

### 引言   
在检索增强生成(RAG)系统中,检索质量直接决定了最终生成结果的准确性和相关性。然而,单一的检索方式往往难以全面捕获用户意图。**当我们使用多个检索系统(如BM25关键词搜索和向量语义搜索)时**,如何有效融合这些不同来源的结果就成为了关键问题。

倒数排序融合(Reciprocal Rank Fusion, RRF)正是为解决这一问题而生的优雅方案。它无需复杂的参数调优,仅依靠排名位置就能智能地合并多个检索结果,让最相关的文档脱颖而出。

### 什么是RRF?
倒数排序融合(RRF)是一种将多个排序结果列表合并为单一排序列表的算法。它最初由滑铁卢大学和Google合作开发,其核心思想非常直观:**在多个检索系统中都排名靠前的文档,往往更具相关性/更重要。**

RRF的最大优势在于:

* 无需分数归一化 - 不同检索系统的评分标准差异巨大(如BM25分数和余弦相似度),RRF直接使用排名位置,避免了复杂的分数标准化问题
* 简单而强大 - 算法实现简单,但在实践中表现出色
* 零样本有效 - 不需要针对特定领域进行训练或调优

### RRF工作原理
核心公式  
RRF通过以下公式计算每个文档的最终得分:
$$RRF_{score}=\sum \frac{1}{k+rank(d)}$$
其中：
* d 表示某个文档
* rank(d) 是文档在某个检索结果列表中的排名位置(从1开始)
* k 是一个常量,通常设为60,用于降低低排名文档的影响
* 求和符号表示对所有包含该文档的结果列表进行累加

**为什么选择k=60?** 

常量k的作用是平滑排名差异。k=60是经过学术研究验证的经验值,它能在以下两点之间取得良好平衡:

* 让高排名文档有明显优势
* 避免低排名文档的贡献完全被忽略

### 直观计算
让我们通过一个例子来理解RRF的工作机制。

假设有三个检索系统返回了以下结果:

系统A: Doc1, Doc2, Doc3, Doc4, Doc5
系统B: Doc3, Doc1, Doc4, Doc6, Doc2
系统C: Doc2, Doc3, Doc1, Doc8, Doc9
计算Doc1的RRF分数(k=60):
```
RRF(Doc1) = 1/(60+1) + 1/(60+2) + 1/(60+3)    
= 1/61 + 1/62 + 1/63         
≈ 0.0164 + 0.0161 + 0.0159         
≈ 0.0484
```
计算Doc3的RRF分数:
```
RRF(Doc3) = 1/(60+3) + 1/(60+1) + 1/(60+2)          
= 1/63 + 1/61 + 1/62         
≈ 0.0159 + 0.0164 + 0.0161       
≈ 0.0484
```
可以看到,Doc1和Doc3在三个系统中都排名靠前,因此获得了相似的高分。而只在单个系统中出现的文档(如Doc6, Doc7)则会得到较低的分数。

### RRF在RAG中的应用场景
1.混合检索融合

这是RRF最典型的应用场景。结合词法搜索和语义搜索的优势:

* BM25关键词搜索 - 擅长精确匹配专有名词、缩写词、特定术语
* 向量语义搜索 - 擅长理解语义相关性、同义词、上下文含义

通过RRF融合,既能捕获精确匹配,又不失语义理解。

2.多查询检索融合

当用户查询较为复杂或模糊时,可以通过LLM生成多个子查询,分别检索后用RRF合并结果。

例如,用户问:"任务分解的挑战是什么?"

可以生成子查询:

* "任务分解面临的主要困难"
* "任务分解的局限性"
* "任务分解实施中的问题"

每个子查询独立检索,然后用RRF融合,确保检索的全面性。

3.多模态检索融合

在处理多模态数据时,可能需要融合:

* 文本检索结果
* 图像检索结果
* 表格检索结果

RRF同样能够有效整合这些异构的排序列表。

### 代码示例
```
import jieba
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

#扩充文档列表，包含更多样化的内容以展示不同检索方法的优势
doc_list = [
    #人工智能基础概念文档
    "人工智能是计算机科学的一个分支，致力于创造能够模拟人类智能的系统。",
    "机器学习是人工智能的一个子领域，专注于开发能从数据中学习的算法。",
    "深度学习是机器学习的一种方法，使用多层神经网络处理复杂数据。",
    "自然语言处理是人工智能的一个分支，研究计算机与人类语言的交互。"
    
    #人工智能应用文档
    "智能助手如小度和天猫精灵使用自然语言处理技术理解用户指令。",
    "自动驾驶汽车利用计算机视觉和深度学习技术识别道路情况。",
    "医疗诊断系统使用机器学习分析患者数据，辅助医生做出诊断决策。",

    #人工智能技术文档
    "大型语言模型如GPT和文心一言能够生成类似人类的文本内容。",
    "计算机视觉技术使机器能够理解和处理视觉信息，如图像和视频。",
    "强化学习是一种机器学习方法，通过奖励和惩罚机制让AI学会做决策。",
    
    #包含相似词但不同主题的文档（用于测试语义检索）
    "人工智能产业在中国快速发展，成为新的经济增长点。",
    "智能手机的普及改变了人们的生活和工作方式。",
]

def chinese_tokenizer(text):
    return list(jieba.lcut(text))


#创建BM25检索器（基于关键词匹配）
#BM25适合精确词汇匹配，对关键词出现频率和文档长度进行加权
bm25_retriever = BM25Retriever.from_texts(
    doc_list,
    metadatas=[{"source":f"doc_{i}"} for i in range(len(doc_list))],
    preprocess_func=chinese_tokenizer
)

bm25_retriever.k = 3#设置返回的文档数量


# 创建嵌入模型
embedding_model = r"../bge-large-zh-v1.5"
embeddings = HuggingFaceEmbeddings(
    model_name=embedding_model,
    model_kwargs={'device': 'cpu'}  # 使用GPU可改为'cuda'
    )


import os
persist_directory = "./chroma_db_custom_3"
if os.path.exists(persist_directory) and os.listdir(persist_directory):
    # 从磁盘加载已有向量库
    print("从磁盘加载已有 Chroma 向量库...")
    chroma_vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
else:
    print(f"从list创建向量数据库...")
    #向量检索适合理解语义相似性，即使没有完全相同的关键词
    chroma_vectorstore = Chroma.from_texts(
    texts=doc_list,#需要嵌入和存储的文本列表
    embedding=embeddings,#用于生成嵌入的嵌入模型实例
    metadatas=metadatas, # 传入metadata列表
    persist_directory="./chroma_db_custom_3"#指定持久化存储向量数据的目录
)

#创建向量检索器
vector_retriever=chroma_vectorstore.as_retriever(search_kwargs={"k":3})

#初始化混合检索器（Ensemble Retriever）
#权重表示各检索器的重要性，这里我们平均分配
#混合检索结合了关键词匹配和语义理解的优势
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.5, 0.5],
    #search_kwargs={"k":3}
)

#定义测试函数，用于比较不同检索器的结果
def compare_retrievers(query):
    print(f"\n查询: '{query}'")
    
    #使用BM25检索器（关键词匹配）
    print("\nBM25检索器结果 (关键词匹配):")
    bm25_docs = bm25_retriever.invoke(query)
    for i,doc in enumerate(bm25_docs):
        print(f"{i+1}. {doc.page_content}")
        
    #使用向量检索器（语义匹配）
    print("\n向量检索器结果 (语义匹配):")
    vector_docs = vector_retriever.invoke(query)
    for i,doc in enumerate(vector_docs):
        print(f"{i+1}. {doc.page_content}")
        
    #使用混合检索器（结合两种方法）
    print("\n混合检索器结果 (关键词+语义):")
    ensemble_docs = ensemble_retriever.invoke(query)
    for i,doc in enumerate(vector_docs):
        print(f"{i+1}. {doc.page_content}")
        


#测试不同类型的查询
print("============ 检索器比较测试 ============")

#测试1: 直接关键词匹配 - BM25应该表现良好
compare_retrievers("深度学习")

#测试2: 语义相关但没有直接关键词 - 向量检索应该表现更好
compare_retrievers("智能系统如何理解人类语言")

#测试3: 混合查询 - 混合检索应该提供最全面的结果
compare_retrievers("人工智能在医疗领域的应用")

#测试4: 歧义查询 - 测试检索器如何处理多义词
compare_retrievers("智能产品")

print("\n============ 测试结束 ============")
```

参考：https://zhuanlan.zhihu.com/p/1914270914654237406