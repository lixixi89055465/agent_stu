from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.tracers import Run


def test1(x: int):
    return x + 10


# 7后备选项
r1 = RunnableLambda(test1)
r2 = RunnableLambda(lambda x: int(x) + 100)
# 在加法计算中的后备选项
chain = r1.with_fallbacks([r2])
print(chain.invoke('2'))

counter = 0


def test3(x):
    global counter
    counter += 1
    print(f'执行了 {counter}次')
    return x / counter


print('1' * 100)
r1 = RunnableLambda(test3).with_retry(stop_after_attempt=4)
print(r1.invoke(2))

r1 = RunnableLambda(test1)
r2 = RunnableLambda(lambda x: [x] * 2)
# 根据r1的输出结果，判断，是否要执行r2,(判断本身也是一个节点）
# chain = r1 | RunnableLambda(lambda x: r2 if x > 12 else RunnablePassthrough().assign(res=x))
chain = r1 | RunnableLambda(lambda x: r2 if x > 12 else RunnableLambda(lambda x: x))
print('2' * 100)
print(chain.invoke(5))
print('3' * 100)
print(chain.invoke(1))


def on_start(run_obj: Run):
    '''当r1节点启动的时候，自动调用 '''
    print('r1启动的时间', run_obj.start_time)


def on_end(run_obj: Run):
    print('r1结束的时间', run_obj.end_time)


chain = r1.with_listeners(on_start=on_start, on_end=on_end)

print('4'*100)
print(chain.invoke(1))
