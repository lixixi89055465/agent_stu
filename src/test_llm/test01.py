from agent.my_llm import llm
resp=llm.invoke('用三句话简单介绍一下：机器学习的基本概念')
print(type(resp))
print(resp)

