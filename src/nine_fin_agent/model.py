from src.nine_fin_agent.config import settings
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    model=settings.model,
    temperature=0,
)