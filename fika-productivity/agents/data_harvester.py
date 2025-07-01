import os
import json
from datetime import datetime
from typing import Dict, Any
from utils.github_api import fetch_recent_commits
from utils.webhook_parser import fetch_webhook_data


def fetch_github_data(state: Dict[str, Any]) -> Dict[str, Any]:
    use_webhook = os.getenv("USE_WEBHOOK", "false").lower() == "true"
    if use_webhook:
        events = fetch_webhook_data()
    else:
        use_live = os.getenv("USE_LIVE_GITHUB", "false").lower() == "true"
        if use_live:
            repo = os.getenv("GITHUB_REPO")
            token = os.getenv("GITHUB_TOKEN")
            events = fetch_recent_commits(repo, token)
        else:
            with open("data/seed_events.json", "r") as f:
                events = json.load(f)

    for event in events:
        if isinstance(event["timestamp"], str):
            event["timestamp"] = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))

    return {"events": events}


def fetch_webhook_data():
    files = sorted(os.listdir("webhooks"), reverse=True)
    events = []
    for file in files[:5]:  # last 5 webhooks
        with open(os.path.join("webhooks", file)) as f:
            data = json.load(f)
            if "commits" in data:
                for c in data["commits"]:
                    events.append({
                        "author": c["author"]["name"],
                        "type": "commit",
                        "additions": c.get("added", []).__len__(),
                        "deletions": c.get("removed", []).__len__(),
                        "files": len(c.get("modified", [])),
                        "timestamp": c["timestamp"]
                    })
    return {"events": events}

