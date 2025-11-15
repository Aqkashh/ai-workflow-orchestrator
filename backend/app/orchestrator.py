from langgraph.graph import StateGraph, END
from langgraph.graph import MessagesState
from typing import TypedDict

from backend.app.data_ingestion_agent import DataIngestionAgent
from backend.app.analysis_agent import AnalysisAgent
from backend.app.report_agent import ReportAgent    
from backend.app.decision_agent import DecisionAgent


class WorkflowState(TypedDict, total=False):
    user_input: str
    ingestion_output: str
    analysis_output: str
    report_output: str
    decision_output: str


ingest_agent = DataIngestionAgent()
analysis_agent = AnalysisAgent()
report_agent = ReportAgent()
decision_agent = DecisionAgent()

async def run_ingestion(state: WorkflowState):
    result = await ingest_agent.run(state["user_input"])
    return {"ingestion_output": result}


async def run_analysis(state: WorkflowState):
    result = await analysis_agent.run(state["ingestion_output"])
    return {"analysis_output": result}


async def run_report(state: WorkflowState):
    result = await report_agent.run(state["analysis_output"])
    return {"report_output": result}


async def run_decision(state: WorkflowState):
    result = await decision_agent.run(state["report_output"])
    return {"decision_output": result}

workflow = StateGraph(WorkflowState)

workflow.add_node("ingestion", run_ingestion)
workflow.add_node("analysis", run_analysis)
workflow.add_node("report", run_report)
workflow.add_node("decision", run_decision)

# Link nodes (sequential flow)
workflow.set_entry_point("ingestion")
workflow.add_edge("ingestion", "analysis")
workflow.add_edge("analysis", "report")
workflow.add_edge("report", "decision")
workflow.add_edge("decision", END)

# Compile graph
app_graph = workflow.compile()

if __name__ == "__main__":
    import asyncio

    user_message = "backend/uploads/test.csv"


    result = asyncio.run(app_graph.ainvoke({"user_input": user_message}))

    print("\n===== FINAL PIPELINE OUTPUT =====")
    print(result)
