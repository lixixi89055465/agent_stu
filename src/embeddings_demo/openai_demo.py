from openai import OpenAI

from agent.env_utils import OPENAI_API_KEY, OPENAI_BASE_URL

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)
text = '明天的天气'
resp = client.embeddings.create(
    model='text-embedding-3-large',
    dimensions=512,
    input=text
)

print(resp.data[0].embedding)
print(len(resp.data[0].embedding))
