# from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI

from agent.env_utils import ALIBABA_API_KEY, ALIBABA_BASE_URL, ZHIPU_API_KEY

# 需求:提示词1--> llm -->文本 --->提示词2--> llm --> 评分
llm = ChatOpenAI(  # 调用大模型
    model="qwen3-max",
    temperature=0.6,
    api_key=ALIBABA_API_KEY,
    base_url=ALIBABA_BASE_URL
)

prompt1 = PromptTemplate.from_template("给我写一篇关于{key_word} 的 {type} ,字数不超过{count}")
prompt2 = PromptTemplate.from_template("请简单评价一下这篇短文，如果总分是10分，请给这篇短文打分:{text_content}")

# 整个需求的第一段,组成一个chain
chain1 = prompt1 | llm | StrOutputParser()
print('1' * 100)
chain2 = chain1 | prompt2 | StrOutputParser()
print('2' * 100)
# str1 = chain1.invoke({'key_word': '青春', 'type': '善文', 'count': 400})
chain2 = prompt2 | llm | StrOutputParser()
print('3' * 100)
# print(str1)
# str2 = chain2.invoke(str1)
print('4' * 100)


# print(str2)


def printchain1(input):
    print(input)
    print('-' * 100)
    return {'text_content': input}


chain2 = chain1 | RunnableLambda(printchain1) | prompt2 | llm | StrOutputParser()

print('5' * 100)
print(chain2.invoke({'key_word': '青春', 'type': '善文', 'count': 400}))
