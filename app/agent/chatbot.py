from app.agent.sql_agent import SQLAgent
from app.vectorstore.store_and_query import query_similar_chunks
from app.config.llm import get_llm_client
from langchain_core.messages import HumanMessage

class DocumentChatbot:
    def __init__(self):
        self.llm = get_llm_client()
        self.sql_agent = SQLAgent()
        self.current_table = None
        self.is_structured_data = False

    def set_document_type(self, is_structured: bool, table_name: str = None):
        """Set document type after processing"""
        self.is_structured_data = is_structured
        self.current_table = table_name

    def answer_query(self, query: str) -> str:
        if self.is_structured_data and self.current_table:
            print(f"🔍 Processing structured query: {query} on table {self.current_table}")
            # Use SQL agent for structured data
            return self.sql_agent.execute_query(query, self.current_table)
        else:
            print(f"🔍 Processing unstructured query: {query}")
            # Use vector search for unstructured data
            # Get relevant chunks
            results = query_similar_chunks(query, top_k=3)
            
            # Construct prompt with context
            context = "\n".join(results['documents'][0]).strip()
            prompt = f"""You are a helpful assistant summarizing issues from a document.
            Based on the following context, answer the question. If the answer is only partially available, do your best to infer from the available content.

            Context:
            {context}

            Question: {query}

            Answer:"""

            
            # Get response from LLM using invoke instead of complete
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            return response.content