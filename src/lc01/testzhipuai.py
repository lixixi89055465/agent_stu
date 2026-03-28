from zhipuai import ZhipuAI

from agent.env_utils import ZHIPU_API_KEY

client = ZhipuAI(api_key=ZHIPU_API_KEY)

with open(f"D:/audio.wav", 'rb') as audio_file:
    transcriptResponse = client.audio.transcriptions.create(
        model='glm-asr',
        file=audio_file,
        stream=False
    )
    print(transcriptResponse.model_extra['text'])
