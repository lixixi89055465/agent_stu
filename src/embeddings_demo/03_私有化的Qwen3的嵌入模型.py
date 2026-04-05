from sentence_transformers import SentenceTransformer

qwen3_embedding = SentenceTransformer('Qwen/Qwen3-Embedding-0.6B')

resp = qwen3_embedding.encode([
    "I like large language models",
    "今天的天气真不错"])

print(resp[0])
print(len(resp[0]))
