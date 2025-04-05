
# 项目开发日志：RAG-QA 智能问答系统

本文件记录项目从构想到实现的整个过程，包括模型选择、架构搭建、实验调试与部署准备。

---

## 🗓项目时间线概览

| 日期        | 阶段                      | 说明                                 |
|-------------|---------------------------|--------------------------------------|
| 2025-03-17  | 立项 & 场景设定           | 定位于企业FAQ问答场景，目标构建RAG系统 |
| 2025-03-18  | 数据构造 & 分块           | 收集并构造模拟FAQ文档，清洗并按问答对分块 |
| 2025-03-19  | 语义向量生成 & 检索构建   | 使用Sentence-BERT生成向量，构建FAISS索引 |
| 2025-03-20  | 回答模型测试              | 尝试T5-small / T5-base / flan-t5-base进行精度对比 |
| 2025-03-21  | 架构封装 & 模块拆分       | 完成retriever/generator/utils模块封装 |
| 2025-03-22  | CLI接口开发               | 添加main.py支持命令行调用问答流程    |
| 2025-03-23  | Colab版本调试完成         | 成功在Colab运行完整流程+GPU部署测试   |
| 2025-03-24  | 项目结构整理 & README撰写 | 整合为GitHub项目，完成文档与交付格式化 |

---

## 模型选择过程

- 初始尝试：`t5-small`，生成质量差，句子模糊
- 第二尝试：`flan-t5-base`，语言自然，结合语境效果明显提升
- 放弃方案：使用 GPT-3.5 API（依赖网络/调用成本，面试中难以自证）

---

## 检索策略对比

| 方法           | Top-3命中率 | 说明 |
|----------------|-------------|------|
| BM25关键词检索 | 68%         | 无法覆盖语义近义问题 |
| MiniLM向量检索 | 91%         | 能识别语言变体，支持相似提问 |

---

## 模块设计说明

- **faiss_search.py**：加载向量模型、生成嵌入、构建FAISS索引并检索
- **answer_gen.py**：负责将检索上下文与提问拼接为Prompt，生成自然语言回答
- **main.py**：命令行入口；集成提问 → 检索 → 生成流程
- **demo_query.ipynb**：Colab运行版，用于展示演示样例

---

## 实验记录样例

### 问题：How do I apply for internship?

检索Top-3文档：
```
[1] Q1: How do I apply for internship opportunities? ...
[2] Q2: What kind of internships are available? ...
[3] Q4: How do I know my application status? ...
```

生成回答：
```
You can apply through our internship portal at internhub.ai/apply and submit your resume.
```

---

## 遇到问题 & 解决方案

| 问题描述                                      | 解决方式                             |
|-----------------------------------------------|--------------------------------------|
| JSONDecodeError 无法读取 split_chunks.json     | 使用 UTF-8 with BOM 重写文件编码      |
| flan-t5 模型加载出错（未识别 encode 方法）     | 切换为 `tokenizer(prompt)` 而非 encode |
| 本地缺少 CUDA 驱动                           | 迁移至 Colab 并启用 GPU 加速         |
| 回答含糊（如“Please check the website.”）     | 将Top文档限制为3条并提升生成 token 长度 |

---

## 性能评估（手工）

| 项目       | 数据 |
|------------|------|
| Top-3 Recall | ≈91% |
| 回答合理性（主观评分） | 4.6 / 5 |
| 推理时延（单轮） | ≈1.1s |
| 启动时间 | 3.8s（含模型加载） |

---

## 未来规划

- 多轮对话支持（历史上下文缓存）
- 引入 Prompt 模板强化回答完整性
- 封装成 API，适配网页调用（FastAPI + Streamlit）

