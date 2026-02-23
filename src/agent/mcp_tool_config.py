gaode_mcp_server_config = {
    # 高德地图MCP服务端 里面有各种高德给你提供公交、地铁、公交、驾车、步行、骑行、POI搜索、IP定位、逆地理编码、云图服务、云图审图、云图审
    "url": "https://mcp.amap.com/mcp?key=b586f1b04ba44e85ea61f37b9fff1680",
    "transport": "streamable_http",
}

# 12306的MCP服务端（工具的配置）
my12306_mcp_server_config = {
    "url": "https://mcp.api-inference.modelscope.net/1d984e337eaa44/mcp",
    "transport": "streamable_http",
}

# 数据分析报表的MCP服务端（工具的配置）
fenxi_mcp_server_config = {
    "url": "https://mcp.api-inference.modelscope.net/91b80b18506548/sse",
    "transport": "sse",
}
