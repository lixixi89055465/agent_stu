import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver  # 1. 导入 SqliteSaver
from langgraph.prebuilt import create_react_agent
from langgraph.store.sqlite import SqliteStore

from agent.models import llm
from agent.tools.tool_demo6 import runnable_tool

with sqlite3.connect('langgraph.db', check_same_thread=False) as conn:
    # 2. 将连接包装进 SqliteSaver
    store = SqliteStore(conn)
    checkpointer = SqliteSaver(conn)
    store.setup()
    checkpointer.setup()

    # checkpointer=InMemorySaver
    agent = create_react_agent(
        llm,
        tools=[runnable_tool],
        prompt='你是一个智能助手，尽可能的调用工具回答用户的问题',
        checkpointer=checkpointer,
        store=store,
    )
    config = {
        'configurable': {
            'thread_id': '1'
        }
    }
    rest = list(agent.get_state(config))  # 从短期存储中，返回所有当前会话的上下文
    print(rest)
    resp1 = agent.invoke(
        {'messages': [{"role": 'user', 'content': "给我一个关于相声的报幕词？"}]},
        config
    )
    print(resp1['messages'][-1].content)
    resp2 = agent.invoke(
        {'messages': [{"role": 'user', 'content': "再给我关于流行歌曲《忐忑》的？"}]},
        config
    )
    print('1' * 100)
    print(resp2['messages'][-1].content)
