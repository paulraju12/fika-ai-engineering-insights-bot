from typing import Dict, Any
from collections import defaultdict
from datetime import timedelta


def analyze_diff(state: Dict[str, Any]) -> Dict[str, Any]:
    events = state.get("events", [])

    total_additions = 0
    total_deletions = 0
    total_files = 0
    commit_count = 0
    pr_count = 0
    ci_failures = 0  # Placeholder for now
    per_author_stats = defaultdict(lambda: {"additions": 0, "deletions": 0, "files": 0, "events": 0})

    for event in events:
        author = event.get("author", "unknown")
        additions = event.get("additions", 0)
        deletions = event.get("deletions", 0)
        files = event.get("files", 0)
        event_type = event.get("type", "")

        if event_type == "commit":
            commit_count += 1
        elif event_type == "pull_request":
            pr_count += 1

        total_additions += additions
        total_deletions += deletions
        total_files += files

        per_author_stats[author]["additions"] += additions
        per_author_stats[author]["deletions"] += deletions
        per_author_stats[author]["files"] += files
        per_author_stats[author]["events"] += 1

    churn = total_additions + total_deletions

    # Flag churn spikes (simple threshold for demo)
    spike_threshold = 500  # Lines
    churn_spike_flag = churn > spike_threshold

    return {
        "commit_count": commit_count,
        "pr_count": pr_count,
        "total_additions": total_additions,
        "total_deletions": total_deletions,
        "total_files": total_files,
        "code_churn": churn,
        "churn_spike": churn_spike_flag,
        "per_author": dict(per_author_stats),
        "ci_failures": ci_failures  # Future implementation
    }
