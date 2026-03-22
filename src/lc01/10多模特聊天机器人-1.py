# 提示词模板
from langchain_community.chat_message_histories import SQLChatMessageHistory,ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.stores import InMemoryStore

from agent.my_llm import llm

# 提示词模板
prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个乐于助人的助手。尽你所能回答所有问题。提供的聊天历史包含与你对话用户的相关信息。'),
    MessagesPlaceholder(variable_name='chat_history', optional=True),
    ('human', '{input}')
])

chain=prompt|llm # 基础的执行链
# 存储聊天记录
store={}
def get_session_history(session_id:str):
    # if session_id not in store:
    #     store[session_id]=ChatMessageHistory()
    # return store[session_id]
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string="sqlite:///chathistory.db"
    )

# 3.创建历史记录功能的处理链
chain_with_message_history=RunnableWithMessageHistory(
    chain,
    get_session_history,

)