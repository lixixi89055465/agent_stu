# 提示词模板
import uuid

from langchain_community.chat_message_histories import SQLChatMessageHistory, ChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnablePassthrough

from agent.my_llm import llm, multiModal_llm
import gradio as gr

# 提示词模板
prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个多模态Ai助手，可以处理文本、音频和图像输入'),
    MessagesPlaceholder(variable_name='messages'),  # 代表：历史消息。
])

chain = prompt | multiModal_llm


def get_session_history(session_id: str):
    ''' 从关系型数据库的历史消息列表中 返回当前会话 的所有历史小i下'''
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string="sqlite:///chat_history.db"
    )


chain_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
)

# user_msg = HumanMessage(content=[{'type': 'text', 'content': '你知道机器学习是什么意思吗'}])
# user_msg = "5除以4等于几"
user_msg = HumanMessage(content=[{'type': 'text', 'text': '你知道机器学习是什么意思吗'}])
config = {'configurable': {'session_id': str(uuid.uuid4())}}
resp1 = chain_history.invoke({'messages': [user_msg]}, config)
print('1' * 100)
print(resp1.content)
