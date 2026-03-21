# from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
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
gather_preferences_prompt = ChatPromptTemplate.from_template(
    '用户输入了一些餐厅偏好:{input1}\n'
    '请将用户䣌偏好总结为清晰的需求:'
)

recommend_restaurants_prompt = ChatPromptTemplate.from_template(
    '基于用户需求:{input2}\n'
    '请推荐 3 家合适的餐厅，并说明推荐理由：'
)
# 步骤3:总结推荐内容供用户快速参考
summarize_recommendations_prompt = ChatPromptTemplate.from_template(
    '以下是餐厅推荐和推荐理由：\n{input3}\n'
    '请总结成 2-3 句话，供用户快速参考:'
)

chain = gather_preferences_prompt | llm | recommend_restaurants_prompt | llm | summarize_recommendations_prompt | llm | StrOutputParser()
r1 = chain.invoke({'input1': '我喜欢安静的地方，有素食的餐厅更好，而且价格也不贵'})
print(r1)
