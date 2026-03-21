# from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough


def test1(x: int):
    return x + 10


# 节点：标准:Runnable

r1 = RunnableLambda(test1)  # 把行数封装成一个组件

res = r1.invoke(4)
print(res)
# 2、批量调用
res = r1.batch([4, 5])
print(res)


# 3、流式调用
def test2(prompt: str):
    for item in prompt.split(' '):
        yield item


r1 = RunnableLambda(test2)  # 把行数封装成一个组件
res = r1.stream('Thisi is a Dog.')
print('1' * 100)
for chunk in res:
    print(chunk)

# 4、组合连
r1 = RunnableLambda(test1)
r2 = RunnableLambda(lambda x: x * 2)
chain1 = r1 | r2
print('2' * 100)
print(chain1.invoke(2))
# 5.并行运行
chain = RunnableParallel(r1=r1, r2=r2)
# max_concurrentcy 最大并发数
print('3' * 100)
print(chain.invoke(2, config={'max_concurrentcy': 1}))
print('4' * 100)
print((chain1 | chain).invoke(2))
new_chain = chain1 | chain
new_chain.get_graph().print_ascii()
print('5' * 100)
print(new_chain.invoke(2))

# 6.合并输入，并处理中间数据
# RunnablePassthrough:  # 允许传递输入数据，可以保持不变或者添加额外的键。必须传入一个字典数据，还可以过滤

r1 = RunnableLambda(lambda x: {'key1': x})
r2 = RunnableLambda(lambda x: x['key1'] + 10)
r3 = RunnableLambda(lambda x: x['new_key']['key2'])
# chain = r1 | r2
# print('6' * 100)
# print(chain.invoke(2))
# chain = r1 | RunnablePassthrough.assign(new_key=r2)
# chain = r1 | RunnablePassthrough() | RunnablePassthrough.assign(new_key=r2)

# chain = r1 | RunnableParallel(foo=RunnablePassthrough(), new_key=RunnablePassthrough.assign(key2=r2))
# chain = r1 | RunnableParallel(foo=RunnablePassthrough(), new_key=RunnablePassthrough.assign(key2=r2)) | \
#         RunnablePassthrough().pick(['new_key'])
chain = r1 | RunnableParallel(foo=RunnablePassthrough(), new_key=RunnablePassthrough.assign(key2=r2)) | \
        RunnablePassthrough().pick(['new_key']) | r3
print('6' * 100)
print(chain.invoke(2))
