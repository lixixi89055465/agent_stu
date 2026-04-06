import ast

import numpy as np
import pandas as pd
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer

from agent.env_utils import OPENAI_API_KEY, OPENAI_BASE_URL

openai_embedding = OpenAIEmbeddings(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    model='qwen3-embed-4b'
)

# BAAI/bge-large-zh-v1.5

model_name = 'BAAI/bge-large-zh-v1.5'
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
# set true to compute cosine similarity
bge_hf_embedding = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
)


def text_2_embedding(text):
    resp = bge_hf_embedding.embed_documents(
        [text])
    return resp[0]


def embedding_2_file(source_file, output_file):
    ''' 读取原始的没事评论数据，通过调用 Embeddingm模型到向量,
    并保持到新文件中'''
    # 步骤:1、准备数据，并读取
    df = pd.read_csv(source_file, index_col=0)
    df = df[['Time', 'ProductId', 'UserId', 'Score', 'Summary', 'Text']]
    print(df.head(2))
    # 步骤2:清洗数据和合并数据
    # df=df.dropna()
    # 把评论的摘要和内存字段合并成一个字段（方便后续处理）
    df['text_content'] = 'Summary:' + df.Summary.str.strip() + "; Text:" + df.Text.str.strip()
    print(df.head(2))  # 增加一个text_content
    # 步驟3：向量化 ，存到一个新的文件中
    df['embedding'] = df.text_content.apply(lambda x: text_2_embedding(x))
    df.to_csv(output_file)


def cosine_distance(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search_text(input, embedding_file, top_n=3):
    '''
    根据用户输入的问题，进行语义检索，返回最相似的前top_n个结果
    :param input:
    :param embedding_file:
    :param top_n:
    :return:Summary:where does one  start...and stop... with a treat like this; Text:Wanted to save some to bring to my Chicago family but my North Carolina family ate all 4 boxes before I could pack. These are excellent...could serve to anyone
    '''
    df_data = pd.read_csv(embedding_file)
    # 把字符串变成向量，保持到新字段
    df_data['embedding_vector'] = df_data['embedding'].apply(
        ast.literal_eval
    )
    input_vector=text_2_embedding(input)
    df_data['similarity']=df_data.embedding_vector.apply(lambda x:cosine_distance(x, input_vector))
    res = (
        df_data.sort_values('similarity', ascending=False).head(top_n)
        .text_content.str.replace('Summary:', '')  # text_content是字段名
        .str.replace('; Text:', ';')
    )
    for r in res:
        print(r)
        print('-' * 30)


if __name__ == '__main__':
    # embedding_2_file('datas/fine_food_reviews_1k.csv', 'datas/output_file.csv')
    search_text('I like juicy barbecued meat.', 'datas/output_file.csv')
