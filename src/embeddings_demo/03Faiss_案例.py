import ast


import faiss
import numpy as np
import pandas as pd
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.docstore import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer

from agent.env_utils import OPENAI_API_KEY, OPENAI_BASE_URL
from embeddings_demo.Embeddings_model import CustomQwen3Embeddings
from embeddings_demo.faiss_demo1 import vector_store

qwen_embedding = CustomQwen3Embeddings('Qwen/Qwen3-Embedding-0.6B')

# 读取数据库数据
FAISS.load_local('../faiss_db', \
                 embeddings=qwen_embedding,
                 allow_dangerous_deserialization=True
                 )
results = vector_store.similarity_search_with_score(query='有美食的内容吗', k=2,
                                                    filter={'source':"news"})
for res, score in results:
    print(type(res))
    print(res.id)
    print(f'* [Score={score:3f}]{res.page_content} [{res.metadata}]')
