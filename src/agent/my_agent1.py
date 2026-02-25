from langchain.agents import create_agent

from agent.my_llm import llm


def send_email(to: str, subject: str, body: str):
    '''发送邮件'''
    email = {
        "to": to,
        "subject": subject,
        "body": body
    }
    # ... 邮件发送逻辑
    return f'邮件已发送至{to}'


agent = create_agent(
    llm,
    tools=[send_email],
    system_prompt='你是一个邮件助手。请始终使用send_email 工具'

)
