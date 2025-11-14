from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableLambda


from backend.app.tools.fetchers import fetch_csv
from backend.app.tools.fetch_api import fetch_api
from backend.app.tools.parse_pdf import parse_pdf   

from dotenv import load_dotenv
load_dotenv()

class DataIngestionAgent:
    def __init__(self):
        self.name="DataIngestionAgent"
        self.role = (
            "You are a Data Ingestion Agent. "
            "Your job is to understand what data the user wants to ingest. "
            "If they provide a CSV file path, use fetch_csv. "
            "If they provide a PDF path, use parse_pdf. "
            "If they provide an API URL, use fetch_api. "
            "Always extract data and return a clean summary."
        )

        self.model=ChatOpenAI(model="gpt-4o-mini", temperature=0.2).bind_tools([
            fetch_csv, 
            fetch_api, 
            parse_pdf
            ])
    
    async def run (self,user_message:str):
        
        pipeline=(
            RunnableLambda(lambda x :[
                SystemMessage(content=self.role),
                HumanMessage(content=x)
            ])
            |self.model
            |RunnableLambda (lambda m :m.content)
        )

        return await pipeline.ainvoke(user_message)

