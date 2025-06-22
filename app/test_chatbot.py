from app.agent.chatbot import DocumentChatbot

def main():
    query = "tell me about this document"
    bot = DocumentChatbot()

    print(f"\n🔍 Asking: {query}")
    answer = bot.answer_query(query)
    print("\n🤖 Answer:")
    print(answer)

if __name__ == "__main__":
    main()
