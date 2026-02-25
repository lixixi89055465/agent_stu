from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(
#     model="gpt-5",
# )
from agent.my_llm import llm

# for chunk in llm.stream("用三句话简单介绍一下:机器学习的基本概念"):
#     print(type(chunk))
#     print(chunk)

resp = llm.invoke("用三句话简单介绍一下:机器学习的基本概念")
print('1' * 100)
print(resp)
resp = llm.invoke("用三句话简单介绍一下:深度学习的基本概念")
print('2' * 100)
print(resp)
