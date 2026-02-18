from langgraph.graph import StateGraph, END
from states import AgentState
from nodes import planner_node, researcher_node, writer_node, reviewer_node, should_continue

# グラフの定義
workflow = StateGraph(AgentState)

# ノードの追加
workflow.add_node("planner", planner_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_node("reviewer", reviewer_node)

# エントリーポイントの設定
workflow.set_entry_point("planner")

# エッジの追加
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "reviewer")

# 条件付きエッジの追加
# Reviewerの後、修正が必要ならWriterに戻り、そうでなければ終了
workflow.add_conditional_edges(
    "reviewer",
    should_continue,
    {
        "writer": "writer",
        "end": END
    }
)

# グラフのコンパイル
app = workflow.compile()

if __name__ == "__main__":
    print("--- 研究エージェント（ロジック強化版）実行 ---")
    # テスト実行: 最大2回の修正を許容
    inputs = {"topic": "2024年のAIエージェント動向", "revision_number": 0, "max_revisions": 3}
    for output in app.stream(inputs):
        for key, value in output.items():
            # ノードの出力を表示（デバッグ用）
            # print(f"Output from {key}: {value}")
            pass
