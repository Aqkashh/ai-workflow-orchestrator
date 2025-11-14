from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableLambda

from dotenv import load_dotenv
load_dotenv()

class DecisionAgent:
    def __init__(self):
        self.name = "DecisionAgent"
        self.role = (
            "You are a Decision/Action Agent. "
            "Your job is to take the business report provided to you "
            "and generate actionable recommendations. "
            "Your output should include: strategic suggestions, next steps, "
            "potential risks, and opportunities. "
            "Focus on real-world business value and clear, actionable items."
        )

        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2
        )

    async def run(self, report_text: str):
        pipeline = (
            RunnableLambda(lambda x: [
                SystemMessage(content=self.role),
                HumanMessage(content=x)
            ])
            | self.model
            | RunnableLambda(lambda m: m.content)
        )

        return await pipeline.ainvoke(report_text)

