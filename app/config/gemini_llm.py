import google.generativeai as genai
from app.config.settings import settings

def get_gemini_client():
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    return genai.GenerativeModel(settings.GEMINI_MODEL)

class GeminiWrapper:
    """Wrapper to make Gemini API compatible with LangChain interface"""
    def __init__(self):
        self.model = get_gemini_client()
    
    def invoke(self, messages):
        # Extract content from HumanMessage
        if hasattr(messages[0], 'content'):
            prompt = messages[0].content
        else:
            prompt = str(messages[0])
        
        response = self.model.generate_content(prompt)
        
        # Create a response object with content attribute
        class Response:
            def __init__(self, text):
                self.content = text
        
        return Response(response.text)