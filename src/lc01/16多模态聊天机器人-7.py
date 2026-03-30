# 提示词模板
import base64
import io
import uuid

from PIL import Image
from langchain_community.chat_message_histories import SQLChatMessageHistory
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


# 语音处理函数=====
def transcribe_audio(audio_path):
    '''
    使用 Base64处理语音转为
    # 目前多模态大模型：支持两个传参方式:1、base64字符串，2、网络访问的url地址（外网的服务器上)
    :param audio_path:
    :return:
    '''
    try:
        with open(audio_path, 'rb') as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        audio_message = {  # 把音频文件，封装成一条消息
            'type': 'audio_url',
            'audio_url': {
                'url': f'data:audio/mp3;base64,{audio_data}',
                'duration': 30  # 单位：秒（帮助模型优化处理）
            }
        }
        return audio_message

    except Exception as e:
        print(e)
        return {}


def transcribe_image(image_path):
    """
    将任意格式的图片转换为base64编码的data URL
    :param image_path: 图片路径
    :return:  包含base64编码的字典
    """
    with Image.open(image_path) as img:
        # 获取原始图片格式（如JPEG/PNG)
        img_format = img.format if img.format else 'JPEG'
        buffered = io.BytesIO()
        # 保留原始格式（避免JPEG强制转换导致透明通道丢失）
        img.save(buffered, format=img_format)
        image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return {
            'type': 'image_url',
            'image_url': {
                'url': f'data:image/{img_format.lower()};base64,{image_data}',
                'detail': 'low'
            }
        }


def submit_messages(history):
    '''提交用户输入的消息，生成机器人回复'''
    user_messages = get_last_user_after_assistant(history)
    print(user_messages)
    content = []  # HumanMessage 的内容
    if user_messages:
        for x in user_messages:
            if isinstance(x['content'], str):  # 文字输入消息
                content.append({'type': 'text', 'text': x['content']})
            elif isinstance(x['content'], tuple):  # 多媒体输入消息
                file_path = x['content'][0]  # 得到多媒体的文件路径
                if file_path.endswith('.wav'):  # 输入的是音频文件
                    pass
                elif file_path.endswith('.jpg') or file_path.endswith('.png') or file_path.endswith('.jpeg'):
                    pass
            else:
                pass


chain_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
)
config = {'configurable': {'session_id': str(uuid.uuid4())}}

user_msg = HumanMessage(content=[{'type': 'text', 'text': '你知道机器学习是什么意思吗'}])
resp1 = chain_history.invoke(input={'message': [user_msg]}, config=config)
print('1' * 100)
print(resp1.content)

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
