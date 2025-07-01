from langgraph.graph import StateGraph
from agents.data_harvester import fetch_github_data
from agents.diff_analyst import analyze_diff
from agents.insight_narrator import generate_insight
from typing import TypedDict, List, Dict, Any


class DevProductivityState(TypedDict):
    events: List[Dict[str, Any]]
    commit_count: int
    pr_count: int
    total_additions: int
    total_deletions: int
    total_files: int
    code_churn: int
    churn_spike: bool
    per_author: Dict[str, Any]
    ci_failures: int
    summary: str
    chart_path: str


def run_graph_flow():
    builder = StateGraph(DevProductivityState)

    builder.add_node("DataHarvester", fetch_github_data)
    builder.add_node("DiffAnalyst", analyze_diff)
    builder.add_node("InsightNarrator", generate_insight)

    builder.set_entry_point("DataHarvester")
    builder.add_edge("DataHarvester", "DiffAnalyst")
    builder.add_edge("DiffAnalyst", "InsightNarrator")

    app = builder.compile()
    output = app.invoke({})
    return output.get("summary"), output.get("chart_path")
