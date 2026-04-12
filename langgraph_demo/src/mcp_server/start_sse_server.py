import logging

from mcp_server.tool_server import server

if __name__ == '__main__':
    server.run(
        transport='sse',
        host='127.0.0.1',
        port=8080,
        log_level='debug',
        path='/sse'
    )
