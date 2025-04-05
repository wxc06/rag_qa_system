from utils.chunk_loader import load_chunks
from retriever.faiss_search import FaissRetriever
from generator.answer_gen import AnswerGenerator

def main():
    # 🔹 加载文本块
    texts, ids = load_chunks("data/split_chunks.json")

    # 🔹 构建检索器
    retriever = FaissRetriever(texts)

    # 🔹 构建回答生成器
    generator = AnswerGenerator()

    print("\n📥 欢迎使用 RAG 智能问答系统")
    while True:
        question = input("\n🧠 请输入问题（输入 q 退出）：\n> ")
        if question.lower() == 'q':
            print("👋 再见！")
            break

        # 🔍 检索上下文
        docs = retriever.search(question, top_k=3)

        # 🧠 生成答案
        answer = generator.generate(question, docs)

        # 📤 输出结果
        print("\n🔍 Top 文档：")
        for i, doc in enumerate(docs, 1):
            print(f"[{i}] {doc[:100]}...")
        print(f"\n🤖 回答：\n{answer}")

if __name__ == "__main__":
    main()
