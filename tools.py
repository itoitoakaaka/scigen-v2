import os
from langchain_community.tools.tavily_search import TavilySearchResults

def get_search_tool():
    """
    Tavily検索ツールを取得する関数。
    APIキーがない場合はモックを返すか、エラーハンドリングを行う。
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    
    if not api_key:
        print("Warning: TAVILY_API_KEY not found. Using mock search.")
        return MockSearchTool()
    
    return TavilySearchResults(max_results=3)

class MockSearchTool:
    """
    APIキーがない場合のモック検索ツール
    """
    def invoke(self, query: str):
        return [
            {"url": "https://example.com/ai-agents", "content": f"Mock result for {query}: AI agents are evolving rapidly in 2024."},
            {"url": "https://example.com/logic-llm", "content": "Recent studies show that multi-agent systems improve logical reasoning."}
        ]
