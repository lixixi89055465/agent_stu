from langchain_ollama import ChatOllama

import env_utils as env_utils

llm = ChatOllama(
    model=env_utils.QWEN38B_MODEL,
    temperature=0.7
)

llm_mini = ChatOllama(
    model=env_utils.OLLAMA_MODEL,
    temperature=0.7
)

if __name__ == '__main__':
    resp=llm.invoke("请告诉我荒野求生怎么生火。")
    print(resp)
    print(type(resp))