from fastapi import FastAPI, Request, HTTPException
import json
import uvicorn
from datetime import datetime
import os

app = FastAPI()
WEBHOOK_DIR = "webhooks"
os.makedirs(WEBHOOK_DIR, exist_ok=True)


@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        payload = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

    # Optional: validate GitHub secret

    # Filter push or pull_request events
    event_type = request.headers.get("x-github-event")
    if event_type not in ["push", "pull_request"]:
        return {"message": "ignored event"}

    # Save for later processing
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(WEBHOOK_DIR, f"{event_type}-{timestamp}.json")
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)

    return {"status": "received", "event": event_type}
