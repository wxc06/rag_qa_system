from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class AnswerGenerator:
    def __init__(self, model_name="google/flan-t5-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cuda")

    def generate(self, question, docs, max_new_tokens=80):
        context = "\n".join(docs)
        prompt = f"""Answer the question based on the context below.

Context:
{context}

Question: {question}
Answer:"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
