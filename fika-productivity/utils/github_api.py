import requests
import os
from datetime import datetime

GITHUB_API_BASE = "https://api.github.com"

def fetch_recent_commits(repo: str, token: str, per_page: int = 10):
    headers = {"Authorization": f"token {token}"}
    url = f"{GITHUB_API_BASE}/repos/{repo}/commits?per_page={per_page}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    commits = response.json()

    events = []
    for commit in commits:
        sha = commit["sha"]
        detail_url = f"{GITHUB_API_BASE}/repos/{repo}/commits/{sha}"
        detail_resp = requests.get(detail_url, headers=headers)
        if detail_resp.status_code != 200:
            continue
        detail = detail_resp.json()
        author = detail["commit"]["author"]["name"]
        stats = detail.get("stats", {})
        events.append({
            "author": author,
            "type": "commit",
            "additions": stats.get("additions", 0),
            "deletions": stats.get("deletions", 0),
            "files": len(detail.get("files", [])),
            "timestamp": detail["commit"]["author"]["date"]
        })

    return events
