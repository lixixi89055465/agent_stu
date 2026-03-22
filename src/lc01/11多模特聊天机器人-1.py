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
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string="sqlite:///chathistory.db"
    )

# 3.创建历史记录功能的处理链
chain_with_message_history=RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key='input',
    history_messages_key='chat_history'
)
# 4.剪辑和摘要上下文，历史记录：保留最近的2条消息，把之前的所有消息西港城摘要
def summarize_messages(current_input):
    '''简介和摘要上下文呢，历史记录'''
    session_id=current_input['config']['configurable']['session_id']
    if not session_id:
        raise ValueError('把必须通过config参数提供 session_id')
    # 获取当前会话的ID 的所有历史聊天记录
    chat_history=get_session_history(session_id)
    stored_messages=chat_history.messages
    # 剪辑消息列表表
    last_two_messages=stored_messages[-2:]
    messages_to_summarize=last_two_messages[:-2]
    summarization_prompt=ChatPromptTemplate.from_messages([
        ('system','请将以下对话历史压缩为一条保留关键信息的摘要消息。'),
        ('placeholder', '{chat_history}'),
        ('human', '请生成包含上述对话核心内容的摘要，保留重要事实和决策'),
    ])
    summarization_chain=summarization_prompt|llm
    #生成摘要
    summary_messages=summarization_chain.invoke({
        'chat_history': messages_to_summarize
    })
    # 重建历史记录：摘要+最后2条原始消息
    chat_history.clear()
    chat_history.add_message(summary_messages)
    for msg in last_two_messages:
        chat_history.add_message(msg)
    return True

result1=chain_with_message_history.invoke({
    'input':'你好，我是张学良'
},config={'configurable':{'session_id':"user123"}})
print(result1)
result2=chain_with_message_history.invoke({
    'input':'我的名字叫什么?'
},config={'configurable':{'session_id':"user123"}})
print(result2)
result3=chain_with_message_history.invoke({
    'input':'历史上，和我同名的人有哪些'
},config={'configurable':{'session_id':"user123"}})
print(result3)

