from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda

from backend.app.tools.fetchers import fetch_csv
from backend.app.tools.fetch_api import fetch_api
from backend.app.tools.parse_pdf import parse_pdf

import json
import os


def detect_input_type(user_input: str):
    user_input = user_input.strip()
    _, ext = os.path.splitext(user_input)
    ext = ext.lower()

    if user_input.startswith("http://") or user_input.startswith("https://"):
        return "api"
    if ext == ".csv":
        return "csv"
    if ext == ".pdf":
        return "pdf"
    return "text"


class DataIngestionAgent:
    def __init__(self):
        self.name = "DataIngestionAgent"

        self.role = (
            "You are a Data Ingestion Agent.\n"
            "Your job is to INGEST DATA using the correct tool.\n"
            "If the input is a CSV, CALL fetch_csv.\n"
            "If PDF → CALL parse_pdf.\n"
            "If API URL → CALL fetch_api.\n"
            "Do NOT answer normally.\n"
            "Your ONLY job is to trigger the RIGHT TOOL.\n"
        )

        # IMPORTANT: new JSON function call format
        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.0,
            response_format={"type": "json_object"}  # <-- REQUIRED FOR RELIABLE TOOL CALLS
        ).bind_tools(
            [fetch_csv, fetch_api, parse_pdf],
            tool_choice="auto"  # let LLM decide but strongly forced by prompt
        )

    def handle_model_output(self, message: AIMessage):

        # 1. If LLM requested a tool → execute it
        if "tool_calls" in message.additional_kwargs:
            call = message.additional_kwargs["tool_calls"][0]
            tool_name = call["name"]
            args = call["arguments"]

            if tool_name == "fetch_csv":
                return fetch_csv(**args)

            if tool_name == "fetch_api":
                return fetch_api(**args)

            if tool_name == "parse_pdf":
                return parse_pdf(**args)

            return f"Unknown tool: {tool_name}"

        # 2. Otherwise return its normal text
        return message.content

    async def run(self, user_input: str):

        input_type = detect_input_type(user_input)

        # STRONG tool forcing instructions
        instruction = f"""
Detected input type: {input_type.upper()}

You MUST call the correct tool.
Do NOT reply with text.
Never answer normally.
Your ONLY valid output is a TOOL CALL.
"""

        pipeline = (
            RunnableLambda(lambda x: [
                SystemMessage(content=self.role + "\n" + instruction),
                HumanMessage(content=user_input)
            ])
            | self.model
            | RunnableLambda(self.handle_model_output)
        )

        return await pipeline.ainvoke({})
