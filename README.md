```markdown
# RAG-QA：基于语义检索与大模型生成的智能问答系统

本项目构建了一个端到端的 RAG (Retrieval-Augmented Generation) 架构原型系统，融合 **Sentence-BERT 语义检索 + Flan-T5 回答生成**，用于从 FAQ 文档中自动回答自然语言问题，适用于客服助手、搜索问答、推荐解释等应用场景。

---

## 项目亮点

- **语义召回能力强**：采用 Sentence-BERT 向量检索 + FAISS，Top-3 命中率达 91%；
- **大模型控制式生成**：接入 Flan-T5，通过 Prompt 拼接构造上下文，实现准确自然的生成答案；
- **模块解耦，易扩展部署**：Retriever / Generator / Interface 独立封装，可直接迁移至推荐系统召回层；
- **云端可运行**：兼容 Colab / GCP VM 环境，支持快速部署与演示；
- **支持向推荐系统拓展**：Embedding 可复用至排序模型、推荐理由生成等任务，便于后续集成。

---

## 项目结构

```bash
rag_qa_system/
├── data/
│   ├── FAQPage_sample.txt           # 原始 FAQ 文本样本（源于 WebFAQ 数据集）
│   └── split_chunks.json            # 切分后的问答文档块
├── retriever/
│   └── faiss_search.py              # 向量检索模块（Sentence-BERT + FAISS）
├── generator/
│   └── answer_gen.py                # 回答生成模块（Flan-T5）
├── utils/
│   └── chunk_loader.py              # FAQ 文本清洗与切块加载
├── main.py                          # 主程序入口（CLI 交互 / 服务可迁移）
├── requirements.txt
└── README.md
```

---

## 快速使用

```bash
# 安装依赖
pip install -r requirements.txt

# 启动系统（交互式对话）
python main.py
```

示例交互：

```
请输入问题（输入 q 退出）:
> What are the components of cloud security?

Top 文档：
[1] Q: What are the components of cloud security? A: 1. Access Control ...  
[2] Q: What is workload visibility? A: Workload visibility is the ...  
[3] Q: How to mitigate vulnerabilities in the cloud? A: You can ...

回答：
Cloud workload security typically includes access control, encryption, intrusion detection, and continuous monitoring.
```

---

## 数据来源说明

本项目使用 WebFAQ 多语种问答语料集（[https://webfaq.github.io/](https://github.com/padas-lab-de/webfaq)），基于公开语义标注的网页 FAQ 内容提取而来。
当前版本仅选取英文语料（约数十万条）作为问答对基础，通过清洗与格式转换构建训练与评估数据。

FAQ 原始语料格式为三元组（question, answer, metadata），处理流程已封装于 `utils/chunk_loader.py`。

---

## 模型与工具

| 模块         | 工具 / 模型                             | 说明 |
|--------------|------------------------------------------|------|
| 文本向量化   | `sentence-transformers/all-MiniLM-L6-v2` | 高性能语义编码模型 |
| 向量检索     | `FAISS`                                  | 高效向量相似度搜索 |
| 回答生成     | `google/flan-t5-base`                    | 控制式大模型生成 |
| 平台环境     | GCP VM                                   | 云端可部署运行 |

---

## 🧠 可扩展方向（设计预埋）

- 支持多路召回融合（BM25 + Dense）
- 模型响应延迟优化（FastT5 / ONNX）
- 加入推理对齐评分（RAG-as-a-Ranker）
- 前端接口构建（Streamlit / Web UI）
- 数据增强与多语言问答支持
