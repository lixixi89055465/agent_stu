from langchain_openai import ChatOpenAI

from agent.env_utils import ALIBABA_API_KEY, ALIBABA_BASE_URL

llm = ChatOpenAI(
    model='qwen-turbo',
    temperature=0.8,
    # api_key="XX",
    api_key=ALIBABA_API_KEY,
    # base_url='http://localhost:6006/v1',
    base_url=ALIBABA_BASE_URL,
    extra_body={'chat_template_kwargs': {'enable_thinking': False}}
)