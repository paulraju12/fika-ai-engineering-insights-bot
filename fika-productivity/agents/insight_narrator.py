from typing import Dict, Any
from datetime import datetime
import os

import churn
import matplotlib.pyplot as plt

CHARTS_DIR = "charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

from agents.forecast import forecast_churn
churn_history = [280, 350, 460, churn]  # sample
next_week = forecast_churn(churn_history)
narrative += f"\n🔮 Forecasted churn next week: {next_week} lines."


def generate_insight(state: Dict[str, Any]) -> Dict[str, Any]:
    churn = state["code_churn"]
    churn_spike = state["churn_spike"]
    commit_count = state["commit_count"]
    pr_count = state["pr_count"]
    ci_failures = state.get("ci_failures", 0)
    per_author = state["per_author"]

    # Basic DORA metrics interpretation
    dora_summary = [
        f"🔁 *Deployment Frequency*: {pr_count} PRs merged this week.",
        f"⏱️ *Lead Time*: Simulated by {commit_count} commits before PRs.",
        f"⚠️ *Change Failure Rate*: {ci_failures} failures (placeholder).",
        f"🚑 *Mean Time to Recovery*: (not tracked yet)."
    ]

    churn_line = f"📊 *Code Churn*: {churn} lines changed. {'🚨 Spike Detected!' if churn_spike else '✅ Healthy'}."

    author_lines = ["👤 *Per Developer Summary:*"]
    for dev, stats in per_author.items():
        author_lines.append(
            f"- {dev}: +{stats['additions']} / -{stats['deletions']}, "
            f"{stats['files']} files, {stats['events']} events"
        )

    # Combine summary
    summary = "\n".join([
        "*📈 Weekly Dev Report*",
        *dora_summary,
        churn_line,
        *author_lines
    ])

    # Generate and save chart (for Slack embed)
    chart_path = generate_churn_chart(per_author)

    return {
        "summary": summary,
        "chart_path": chart_path
    }


def generate_churn_chart(per_author: Dict[str, Any]) -> str:
    authors = list(per_author.keys())
    additions = [per_author[dev]["additions"] for dev in authors]
    deletions = [per_author[dev]["deletions"] for dev in authors]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(authors, additions, label='Additions', color='green')
    ax.bar(authors, deletions, label='Deletions', color='red', bottom=additions)
    ax.set_ylabel('Lines of Code')
    ax.set_title('Code Churn per Developer')
    ax.legend()

    chart_filename = f"churn_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    chart_path = os.path.join(CHARTS_DIR, chart_filename)
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    # Convert to relative path (for local testing or serving)
    return f"http://localhost:3000/static/{chart_filename}"  # Or just chart_path if sent to Slack directly
