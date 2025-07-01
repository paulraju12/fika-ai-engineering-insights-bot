# serve_chart.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="charts"), name="charts")

# Run with: uvicorn serve_chart:app --port 3000
