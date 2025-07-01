from slack_bolt import App
from slack_sdk import WebClient
import os
from dotenv import load_dotenv
from langgraph_flow import run_graph_flow

load_dotenv()

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

@app.command("/dev-report")
def handle_dev_report(ack, respond, body):
    ack()

    # Run your LangGraph flow
    summary, chart_path = run_graph_flow()

    # Upload chart image
    try:
        result = client.files_upload(
            channels=body["channel_id"],
            initial_comment=summary,
            file=chart_path,
            title="Code Churn Chart"
        )
        respond("✅ Report posted!")
    except Exception as e:
        respond(f"⚠️ Failed to upload chart: {str(e)}")

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
