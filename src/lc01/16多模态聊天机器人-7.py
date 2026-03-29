# 提示词模板
import uuid

from langchain_community.chat_message_histories import SQLChatMessageHistory
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


def get_last_user_after_assistant(history):
    '''反向便利找到最后一个assistant的位置，并返回后面的所有user消息'''
    if not history:
        return None
    if history[-1]['role'] == 'assistant':
        return None
    last_assistant_idx = -1
    for i in range(len(history) - 1, -1, -1):
        if history[i]['role'] == 'assistant':
            last_assistant_idx = i
            break
    # 如果没有找到assistant
    if last_assistant_idx == -1:
        return history
    else:
        return history[last_assistant_idx + 1:]


def get_session_history(session_id: str):
    ''' 从关系型数据库的历史消息列表中 返回当前会话 的所有历史小i下'''
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string="sqlite:///chat_history.db"
    )


def add_message(chat_history, user_message):
    ''' 将用户输入的消息添加到聊天记录中'''
    # for m in user_message['files']:
    #     print(m)
    #     chat_history.append({'role': 'user', 'content': {'path': m}})
    # # 处理文本消息
    # if user_message['text'] is not None:
    #     chat_history.append({'role': 'user', 'content': {'text': user_message['text']}})
    # return chat_history, gr.MultimodalTextbox(value=None, interactive=False)  # 返回更新后的历史和重置的输入框
    if user_message:
        chat_history.append({'role': 'user', 'content': user_message})
    return chat_history, gr.Textbox(value=None, interactive=False)  # 返回更新后的历史和重置的输入框


def submit_messages(history):
    '''提交用户输入的消息，生成机器人回复'''
    user_messages = get_last_user_after_assistant(history)
    print(user_messages)


chain_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
)
config = {'configurable': {'session_id': str(uuid.uuid4())}}

with gr.Blocks(title='多模态聊天机器人', theme=gr.themes.Soft()) as block:
    # 聊天历史记录的组件
    chatbot = gr.Chatbot(type='messages', height=500, label='聊天机器人', bubble_full_width=False)
    # 创建多模态输入框
    chat_input = gr.MultimodalTextbox(
        interactive=True,  # 可交互
        file_types=['image', '.wav', '.mp4'],
        file_count='multiple',  # 允许多文件上传
        placeholder='请输入信息或者上传文件...',  # 输入框提升文本
        show_label=False,  # 不显示标签
        sources=['microphone', 'upload'],  # 支持麦克风和文件上传
    )
    chat_input.submit(
        add_message,
        [chatbot, chat_input],
        [chatbot, chat_input]
    ).then(
        submit_messages,
        [chatbot],
        [chatbot]
    )
