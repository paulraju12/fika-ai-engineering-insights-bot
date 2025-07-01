# 🤖 FIKA AI Productivity Insights Bot

A Slack-based AI productivity assistant that analyzes GitHub engineering activity using LangGraph agents, forecasts churn, and posts weekly insight reports — all inside chat.

---

## 🚀 Challenge Summary

This is my submission for the **FIKA AI Research — Engineering Productivity Intelligence MVP Challenge**.

The bot provides a chat-first view of engineering output, mapping raw commit/PR data into business insights using LangChain + LangGraph agents.

---

## 🧠 Architecture Diagram

```mermaid
graph TD
    A[Slack /dev-report] --> B[LangGraph Flow]
    B --> C[DataHarvester Agent]
    C --> D[DiffAnalyst Agent]
    D --> E[InsightNarrator Agent]
    E --> F[Slack Response: Chart + Summary]

