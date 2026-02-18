from typing import Dict, Any, Literal
from langchain_core.messages import HumanMessage, SystemMessage
from states import AgentState
from prompts import PLANNER_PROMPT, RESEARCHER_PROMPT, WRITER_PROMPT, REVIEWER_PROMPT
from tools import get_search_tool

# LLMのセットアップ（実環境用）
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(model="gpt-4o", temperature=0)

def planner_node(state: AgentState) -> Dict[str, Any]:
    print("--- 計画ノード (Planner) ---")
    topic = state["topic"]
    
    # 実際のLLM呼び出し例:
    # messages = [
    #     SystemMessage(content=PLANNER_PROMPT),
    #     HumanMessage(content=f"トピック: {topic}")
    # ]
    # response = llm.invoke(messages)
    # plan = response.content
    
    # モック動作
    print(f"   [System Prompt] {PLANNER_PROMPT[:50]}...")
    plan = f"1. {topic} の背景と現状\n2. {topic} の技術的課題\n3. 将来展望と結論"
    return {"plan": plan}

def researcher_node(state: AgentState) -> Dict[str, Any]:
    print("--- 調査ノード (Researcher) ---")
    plan = state["plan"]
    
    # ツールを使用して検索
    search_tool = get_search_tool()
    try:
        # 計画に基づいてクエリを生成するのが理想的だが、ここでは単純にトピックを検索
        # 本番ではLLMにクエリを生成させる: query = llm.invoke(f"Generate search query for: {plan}").content
        query = f"{state['topic']} research agents"
        print(f"   [検索実行] Query: {query}")
        search_results = search_tool.invoke(query)
        
        # 結果を整形
        results = [f"Source: {res['url']}\nContent: {res['content']}" for res in search_results]
    except Exception as e:
        print(f"   [検索エラー] {e}")
        results = ["検索に失敗しました。"]

    return {"search_results": results}

def writer_node(state: AgentState) -> Dict[str, Any]:
    print("--- 執筆ノード (Writer) ---")
    topic = state["topic"]
    results = state["search_results"]
    critique = state.get("critique")
    revision_number = state.get("revision_number", 0)

    # 実際のLLM呼び出し例
    # context = f"調査結果: {results}\n\n以前の批評: {critique}" if critique else f"調査結果: {results}"
    # messages = [
    #     SystemMessage(content=WRITER_PROMPT),
    #     HumanMessage(content=f"トピック: {topic}\n\n{context}")
    # ]
    # response = llm.invoke(messages)
    # draft = response.content

    if critique:
        print(f"   [修正中] リビジョン: {revision_number + 1}")
        draft = f"# {topic} (Rev {revision_number + 1})\n\n[Writer Prompt Logic] 指摘「{critique}」を反映して修正。\n根拠データ: {results[:1]}...\n(論理的整合性を向上させました)"
    else:
        print("   [新規作成]")
        draft = f"# {topic}\n\n[Writer Prompt Logic] 調査結果に基づいて論理的に構成。\n{results[:1]}..."
    
    return {"draft": draft, "revision_number": revision_number + 1}

def reviewer_node(state: AgentState) -> Dict[str, Any]:
    print("--- レビューノード (Reviewer) ---")
    draft = state["draft"]
    revision_number = state.get("revision_number", 1)
    max_revisions = state.get("max_revisions", 2)

    # 実際のLLM呼び出し例
    # messages = [
    #     SystemMessage(content=REVIEWER_PROMPT),
    #     HumanMessage(content=f"以下のドラフトをレビューしてください:\n\n{draft}")
    # ]
    # response = llm.invoke(messages)
    # critique = response.content

    print(f"   [System Prompt] {REVIEWER_PROMPT[:50]}...")

    if revision_number < max_revisions:
        critique = "第2章のデータソースが不明確です。参考文献を追加してください。"
        print(f"   [レビュー結果] 修正が必要です: {critique}")
        return {"critique": critique}
    else:
        print("   [レビュー結果] 承認 (Approval)")
        return {"critique": None}

def should_continue(state: AgentState) -> Literal["writer", "end"]:
    critique = state.get("critique")
    if critique:
        return "writer"
    return "end"
