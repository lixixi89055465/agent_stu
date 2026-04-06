from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from agent.env_utils import OPENAI_BASE_URL, OPENAI_API_KEY, ALIBABA_API_KEY, ALIBABA_BASE_URL

llm = ChatOpenAI(
    model='qwen-turbo',
    temperature=0.8,
    # api_key="XX",
    api_key=ALIBABA_API_KEY,
    # base_url='http://localhost:6006/v1',
    base_url=ALIBABA_BASE_URL,
    extra_body={'chat_template_kwargs': {'enable_thinking': False}}
)


def get_weather(city: str) -> str:
    '''get weather for a given city'''
    return f"It's always sunny in {city}"


graph = create_react_agent(
    llm,
    tools=[get_weather],
    prompt='You are a helpful assistant'
)
