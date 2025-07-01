import schedule
import time
from langgraph_flow import run_graph_flow
from slack_sdk import WebClient
import os
from dotenv import load_dotenv

load_dotenv()
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
CHANNEL_ID = os.getenv("SLACK_CHANNEL", "#general")

def post_scheduled_summary():
    summary, chart_path = run_graph_flow()
    client.files_upload(
        channels=CHANNEL_ID,
        initial_comment=f"📅 *Scheduled Weekly Summary*\n\n{summary}",
        file=chart_path,
        title="Weekly Productivity Chart"
    )

# Run every Monday at 9am
schedule.every().monday.at("09:00").do(post_scheduled_summary)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
