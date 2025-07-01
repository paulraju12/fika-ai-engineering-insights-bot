import os
import json
from datetime import datetime
from typing import List, Dict

WEBHOOK_DIR = "webhooks"

def fetch_webhook_data(max_files: int = 10) -> List[Dict]:
    if not os.path.exists(WEBHOOK_DIR):
        return []

    files = sorted(
        [f for f in os.listdir(WEBHOOK_DIR) if f.endswith(".json")],
        reverse=True
    )

    events = []

    for file in files[:max_files]:
        with open(os.path.join(WEBHOOK_DIR, file)) as f:
            data = json.load(f)

        if "commits" in data:
            # Push event
            for commit in data["commits"]:
                timestamp = commit.get("timestamp", datetime.now().isoformat())
                events.append({
                    "author": commit["author"]["name"],
                    "type": "commit",
                    "additions": len(commit.get("added", [])),
                    "deletions": len(commit.get("removed", [])),
                    "files": len(commit.get("modified", [])),
                    "timestamp": timestamp
                })

        elif "pull_request" in data:
            # PR event
            pr = data["pull_request"]
            timestamp = pr.get("created_at", datetime.now().isoformat())
            events.append({
                "author": pr["user"]["login"],
                "type": "pull_request",
                "additions": pr.get("additions", 0),
                "deletions": pr.get("deletions", 0),
                "files": pr.get("changed_files", 0),
                "timestamp": timestamp
            })

    return events
