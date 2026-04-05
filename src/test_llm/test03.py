import requests
from dashscope import Generation
import dashscope

# 1. 配置 API Key
dashscope.api_key = "sk-33e9967ca2ad4c178693adc0967cad60"

# 2. 创建 Session 对象 (用于连接复用，提升同步调用效率)
# 这相当于在 HTTP 层面保持“长连接”同步状态
session = requests.Session()

try:
    # 3. 同步调用
    # 注意：这里没有传入 'X-DashScope-Async' 头，默认即为同步模式
    response = Generation.call(
        model='qwen-plus',
        prompt='你好，请介绍一下你自己',
        session=session  # 传入 session 实现连接复用
    )

    # 4. 处理同步返回的结果
    if response.status_code == 200:
        print(response.output.text)
    else:
        print(f"请求失败: {response.code}, {response.message}")

finally:
    # 5. 关闭 Session
    session.close()