from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    """
    エージェントの状態を定義するクラス。
    各ノード間で共有される情報を保持します。
    """
    topic: str  # 研究トピック
    plan: Optional[str]  # 研究計画 (Outline)
    search_results: Optional[List[str]]  # 検索結果のリスト
    draft: Optional[str]  # 執筆されたドラフト
    critique: Optional[str]  # レビュー結果（批評）
    revision_number: int  # 現在の修正回数
    max_revisions: int  # 最大修正回数
