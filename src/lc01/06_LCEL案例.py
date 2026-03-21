# from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough, RouterRunnable, \
    RunnableSequence
from langchain_openai import ChatOpenAI

from agent.env_utils import ALIBABA_API_KEY, ALIBABA_BASE_URL, ZHIPU_API_KEY

# 需求:提示词1--> llm -->文本 --->提示词2--> llm --> 评分
llm = ChatOpenAI(  # 调用大模型
    model="qwen3-max",
    temperature=0.6,
    api_key=ALIBABA_API_KEY,
    base_url=ALIBABA_BASE_URL
)
# 定义物理任务模板
physics_template = ChatPromptTemplate.from_template(
    '你是一位物理学教授，擅长用简洁易懂的方式回答物理问题。以下是问题内容:{input}'
)

# 定义数学任务模板
math_template = ChatPromptTemplate.from_template(
    '你是一位数学学教授，擅长用简洁易懂的方式回答数学问题。以下是问题内容:{input}'
)

# 定义历史务模板
history_template = ChatPromptTemplate.from_template(
    '你是一位历史学教授，擅长用简洁易懂的方式回答历史问题。以下是问题内容:{input}'
)

# 定义计算机任务模板
computerscience_template = ChatPromptTemplate.from_template(
    '你是一位计算机学教授，擅长用简洁易懂的方式回答计算机问题。以下是问题内容:{input}'
)
# 默认模板
default_template = ChatPromptTemplate.from_template(
    '输入内容无法归类，请直接回答:{input}'
)
default_chain = default_template | llm
physicst_chain = physics_template | llm
math_chain = math_template | llm
history_chain = history_template | llm
computerscience_chain = computerscience_template | llm


# 动态路由的chain
def route(input):
    if '物理' in input['type']:
        print('1号')
        return {'key': 'physics', 'input': input['input']}
    elif '数学' in input['type']:
        print('2号')
        return {'key': 'math', 'input': input['input']}

    elif '历史' in input['type']:
        print('3号')
        return {'key': 'history', 'input': input['input']}

    elif '计算机' in input['type']:
        print('4号')
        return {'key': 'computer_science', 'input': input['input']}
    else:
        print('5号')
        return {'key': 'default', 'input': input['input']}


# 创建一个路由节点
route_runnable = RunnableLambda(route)

# 路由调度器
router = RouterRunnable(runnables={
    'physics': physicst_chain,
    'math': math_chain,
    'history': history_chain,
    'computer_science': computerscience_chain,
    'default': default_chain,
})

# 第一个提示词模板：
first_prompt = ChatPromptTemplate.from_template(
    """不要回答下面用户的问题,只要根据用户户的输入来判断分类，一共有[物理,历史,计算机,数学,其他]5种类别。\n\n
    用户的输入:{input}\n\n\
    最后的输出包含分类的类别和用户输入的内容，输出格式为json.其中，类别的key为type，用户输入内容的key为input
        """
)
chain1 = first_prompt | llm | JsonOutputParser()
chain2 = RunnableSequence(chain1, route_runnable, router)  # chain=chain1 | route_runnable|router(Runnable)
inputs = [
    {'input': '什么是黑体辐射?'},  # 物理问题
    {'input': '计算2+2的结果?'},  # 数学问题
    {'input': '介绍第一次世界大战的背景.?'},  # 历史问题
    {'input': '如何实现快速排序算法?'},  # 计算机科学问题
]
for inp in inputs:
    result = chain2.invoke(inp)
    print('1' * 100)
    print(f'问题:{inp},\n回答:{result}')
