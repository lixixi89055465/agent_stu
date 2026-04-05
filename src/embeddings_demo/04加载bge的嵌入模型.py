from langchain.embeddings import HuggingFaceBgeEmbeddings
# pip install transformers
# pip install sentence-transformers
# pip install  huggingface_hub langchain-huggingface
# HF_HOME=指定下载目录

model_name = 'BAAI/bge-small-zh-v1.5'
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
bge_hf_embedding = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
)
# model.query_instruction = '为这个句子生成表示以用于检索相关文章'
resp = bge_hf_embedding.embed_documents(
    ['I like large language models.',
     '今天的天气非常不错'
     ]
)
print(resp[0])
print(len(resp[0]))
