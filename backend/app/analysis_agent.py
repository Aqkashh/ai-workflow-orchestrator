from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
load_dotenv()

class AnalysisAgent:
    def __init__(self):
        self.name = "AnalysisAgent"
        self.role = (
            "You are an Analysis Agent. "
            "You analyze ingested data and extract meaningful insights. "
            "If data is numeric (like CSV), find trends, patterns, and anomalies. "
            "If data is text (like PDF), find key points, topics, and sentiment. "
            "If data comes from an API, summarize structure and key values. "
            "Always return a clear, structured analysis summary."
        )

        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2
        )

    async def run(self, ingested_data: str):
        pipeline = (
            RunnableLambda(lambda x: [
                SystemMessage(content=self.role),
                HumanMessage(content=x)
            ])
            | self.model
            | RunnableLambda(lambda m: m.content)
        )

        return await pipeline.ainvoke(ingested_data)