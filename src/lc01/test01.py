# from funasr import AutoModel
# from funasr.utils.postprocess_utils import rich_transcription_postprocess
#
# model_dir = "iic/SenseVoiceSmall"
#
# model = AutoModel(
#     model=model_dir,
#     trust_remote_code=True,
#     remote_code="./model.py",
#     vad_model="fsmn-vad",
#     vad_kwargs={"max_single_segment_time": 30000},
#     device="cuda:0",
# )
#
# # en
# res = model.generate(
#     input=f"{model.model_path}/example/en.mp3",
#     cache={},
#     language="auto",  # "zn", "en", "yue", "ja", "ko", "nospeech"
#     use_itn=True,
#     batch_size_s=60,
#     merge_vad=True,  #
#     merge_length_s=15,
# )
# text = rich_transcription_postprocess(res[0]["text"])
# print(text)

# from zhipuai import ZhipuAI


# client = ZhipuAI()  # 填写您自己的API key
# with open('asr1.wav', 'rb') as audio_file:
#     transcriptResponse = client.audio.transcriptions.create(
#         model='glm-asr',
#         file=audio_file,
#         stream=False
#     )
#     for item in transcriptResponse:
#         print(item)
