# SciGen-v2

Research logic reinforcement agent using LangGraph.

## 🎯 Overview
博士論文（水中環境下の感覚運動制御）の執筆を支援するために設計された、自己反省（Reflexion）ループ搭載のAIエージェント。単なる文章生成ではなく、論理の穴を特定し、自律的に修正することを目指す。

## 🚀 Quick Start
```bash
# 1. Clone the repository
git clone https://github.com/itoitoakaaka/scigen-v2.git

# 2. Setup environment variables
cp .env.example .env  # APIキーを設定

# 3. Run with Docker
docker-compose up --build
```

### 🛠 Architecture
*   **Planner**: 構成案の作成
*   **Researcher**: Tavily APIを用いた先行研究調査
*   **Writer**: ドラフト執筆
*   **Reviewer**: 論理的整合性のチェックと修正指示
