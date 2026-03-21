# 提示词模板
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 提示词模板
prompt = ChatPromptTemplate.from_messages([
    {'system': '你是一个乐于助人的助手。尽你所能回答所有问题。提供的聊天历史包含与你对话用户的相关信息。'},
    MessagesPlaceholder(variable_name='chat_history', optional=True),
    ('human', '{input}')
])
