# 提示词模板
import uuid

from langchain_community.chat_message_histories import SQLChatMessageHistory, ChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnablePassthrough

from agent.my_llm import llm
import gradio as gr

# 提示词模板
prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个乐于助人的助手。尽你所能回答所有问题。提供的聊天历史包含与你对话用户的相关信息。'),
    MessagesPlaceholder(variable_name='chat_history', optional=True),
    ('human', '{input}')
])

chain = prompt | llm  # 基础的执行链
# 存储聊天记录
store = {}


def get_session_history(session_id: str):
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string="sqlite:///chathistory.db"
    )


# 3.创建历史记录功能的处理链
chain_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
)
config = {'configurable': {'session_id': str(uuid.uuid4())}}


# user_msg = HumanMessage(content=[{'type': 'text', 'text': '你知道机器学习是什么吗?'}])
# resp1 = chain_history.invoke({
#     'message': [user_msg]}, config)
# print('0' * 100)
# print(resp1)

def add_message(history, messages):
    ''' 将用户输入的消息添加到聊天记录中 '''
    for m in messages['files']:
        print(m)
        history.append({'role': 'user', 'content': {'path': m}})
    # 处理文本消息
    if messages['text'] is not None:
        print(messages['text'])
        history.append({'role': 'user', 'content': messages['text']})

    return history, gr.MultimodalTextbox(value=None, interactive=False)  # 返回更新后的历史和重置的输入框


def get_last_user_after_assistant(history):
    ''' 反向遍历找到最后一个assistant 的位置，并返回后面的所有user消息 '''
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
        # 从assistant 位置向后查找第一个user
        return history[last_assistant_idx + 1:]


def submit_messages(history):
    '''提交用户输入的消息，生成机器人回复 '''
    print('2' * 100)
    print(history)
    user_messages = get_last_user_after_assistant(history)
    print('3'*100)
    print(user_messages)


# 开发一个聊天机器人的web界面
with gr.Blocks(title='多模态聊天机器人', theme=gr.themes.Soft()) as block:
    # 聊天历史记录的组件
    chatbot = gr.Chatbot(type='messages', height=500, label='聊天机器人',
                         bubble_full_width=False)
    # 创建多模态输入框
    chat_input = gr.MultimodalTextbox(
        interactive=True,  # 可交互
        file_types=['image', '.wav', '.mp4'],
        file_count='multiple',  # 允许多文件上传 ,
        placeholder='请输入信息或者上传文件...',  # 输入框提示文本
        show_label=False,  # 不显示标签
        sources=['microphone', 'upload']  # 支持麦克风和文件上传
    )
    chat_input.submit(
        add_message,
        [chatbot, chat_input],
        [chatbot, chat_input]
    ).then(
        submit_messages,
        [chatbot],
        [chatbot],
    )

if __name__ == '__main__':
    block.launch()
