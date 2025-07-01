from langgraph_flow import run_graph_flow

if __name__ == "__main__":
    summary, chart_path = run_graph_flow()
    print("Summary:\n", summary)
    print("Chart saved at:", chart_path)
