import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(ROOT_DIR)

import streamlit as st
from app.ingestion.processor import process_document
from app.agent.chatbot import DocumentChatbot


def main():
    st.set_page_config(page_title="📄 Document Q&A Chatbot", layout="wide")
    st.title("📄 Document Q&A Chatbot")

    # Initialize chatbot
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = DocumentChatbot()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.markdown("Upload a single Excel or PDF file. Once processed, you can ask any question based on its content.")

    # --- Upload Section ---
    with st.expander("📤 Upload Document", expanded=True):
        uploaded_file = st.file_uploader("Upload a single PDF or Excel file", type=["pdf", "xlsx", "xls", "csv"])

        if uploaded_file:
            temp_path = os.path.join("temp", uploaded_file.name)
            os.makedirs("temp", exist_ok=True)

            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            try:
                st.info("Processing document...")
                is_structured, table_name = process_document(temp_path)
                st.session_state.chatbot.set_document_type(is_structured=is_structured, table_name=table_name)
                st.success(f"✅ Successfully processed: `{uploaded_file.name}`")
                # Optional: clear old messages on new file upload
                st.session_state.messages = []
            except Exception as e:
                st.error(f"❌ Error processing document: {e}")
            finally:
                os.remove(temp_path)

    # --- Chat Section ---
    st.divider()
    st.subheader("💬 Ask Your Questions")

    # Display past messages (preserves history)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept new user input
    if prompt := st.chat_input("Ask a question about the uploaded document"):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response with spinner
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    response = st.session_state.chatbot.answer_query(prompt)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.markdown(response)
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    st.warning("Make sure a valid document is uploaded before asking questions.")

if __name__ == "__main__":
    main()
