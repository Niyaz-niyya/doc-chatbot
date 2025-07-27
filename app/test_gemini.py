from app.config.llm import get_llm_client
from langchain_core.messages import HumanMessage

def test_gemini():
    llm = get_llm_client()
    messages = [HumanMessage(content="Explain how AI works in a few words")]
    response = llm.invoke(messages)
    print("Gemini Response:", response.content)

if __name__ == "__main__":
    test_gemini()