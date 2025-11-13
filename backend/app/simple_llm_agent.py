from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
from app.tools.fetchers import fetch_csv
from app.tools.fetch_api import fetch_api
from app.tools.parse_pdf import parse_pdf



load_dotenv()

class SimpleLLMAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

        # LLM model (Runnable)
        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2
        ).bind_tools([fetch_csv, fetch_api,parse_pdf])
    async def run(self, message: str):
        """Run the agent using Runnable LCEL pipeline."""
        
        # Build a pipeline:
        # SYSTEM PROMPT → USER MESSAGE → LLM → TEXT OUTPUT
        pipeline = (
            RunnableLambda(lambda x: [
                SystemMessage(content=self.role),
                HumanMessage(content=x)
            ])
            | self.model
            | RunnableLambda(lambda m: m.content)
        )

        # Async invoke
        response = await pipeline.ainvoke(message)
        return response


if __name__ == "__main__":
    import asyncio
    
    agent = SimpleLLMAgent(
        "ChatAgent",
        "You are a friendly assistant. You can use tools to read CSV files or fetch APIs."
    )

    result = asyncio.run(agent.run("Hello, who are you?"))
    print("AI says:", result)
