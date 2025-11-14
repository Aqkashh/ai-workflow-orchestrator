from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv  
load_dotenv()

class ReportAgent:
    def __init__(self):
        self.name = "ReportAgent"
        self.role = (
            "You are a Report Generation Agent. "
            "Your job is to take the analysis data provided to you and convert it into a "
            "clear, well-structured, human-readable business report. "
            "Write in a professional tone. Use headings, bullet points, and summaries. "
            "Focus on clarity and readability. "
            "Do NOT repeat raw data — convert it into insights."
        )

        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2
        )
    async def run(self, analysis_text: str):
        pipeline = (
            RunnableLambda(lambda x: [
                SystemMessage(content=self.role),
                HumanMessage(content=x)
            ])
            | self.model
            | RunnableLambda(lambda m: m.content)
        )

        return await pipeline.ainvoke(analysis_text)
