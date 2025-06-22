from langchain_openai import AzureChatOpenAI
from app.config.settings import settings

def get_llm_client():
    return AzureChatOpenAI(
        deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,  
        api_key=settings.AZURE_OPENAI_KEY,              
        api_version=settings.AZURE_OPENAI_API_VERSION,
    )
