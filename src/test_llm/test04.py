import dashscope
import base64
import os

# 1. 配置 API Key
# 建议设置环境变量，或者在这里直接填入 "sk-xxx"
dashscope.api_key = "sk-33e9967ca2ad4c178693adc0967cad60"

# 2. 定义本地文件路径
# 请确保这个文件真实存在
audio_file_path = "src/agent/audio.wav"


# 3. 将本地文件转换为 Base64
def file_to_base64(file_path):
    with open(file_path, "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode("utf-8")
    # 获取文件扩展名用于构建 mime_type
    ext = os.path.splitext(file_path)[1].lower()
    mime_type = f"audio/{ext.replace('.', '')}"
    if ext == ".mp3":
        mime_type = "audio/mpeg"
    elif ext == ".wav":
        mime_type = "audio/wav"
    elif ext == ".aac":
        mime_type = "audio/aac"
    return mime_type, encoded_string


try:
    mime_type, base64_data = file_to_base64(audio_file_path)

    # 4. 构建消息体
    # 注意：data 字段直接填入 base64 字符串，不需要加 "data:audio/mp3;base64," 前缀
    messages = [
        {
            "role": "user",
            "content": [
                {"audio": base64_data},  # 这里填入纯 Base64 字符串
                {"text": "这段音频里的人在说什么？请用中文总结。"}
            ]
        }
    ]

    # 5. 调用模型
    print("正在分析音频...")
    response = dashscope.MultiModalConversation.call(
        model="qwen3-max",
        messages=messages,
        result_format="message"
    )

    # 6. 处理结果
    if response.status_code == 200:
        print("\n✅ 模型回答：")
        print(response.output.choices.message.content.text)
    else:
        print(f"❌ 请求失败: {response.code} - {response.message}")

except FileNotFoundError:
    print(f"❌ 错误：找不到文件 {audio_file_path}，请检查路径。")
except Exception as e:
    print(f"❌ 发生异常: {e}")