# doc-chatbot

A document-based chatbot that allows users to upload PDF or Excel files, stores their content in a vector database or SQL database, and answers user queries using Azure OpenAI and semantic search.

---

## Features

- Upload PDF, Excel, or CSV files via a web UI (Streamlit)
- PDF/Excel content is chunked and stored in a vector database (ChromaDB) or PostgreSQL (for structured data)
- Natural language queries are answered using Azure OpenAI (GPT) and semantic search or SQL agent
- Supports both unstructured (PDF) and structured (Excel/CSV) data
- Modern chat interface with history

---

## Setup

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd doc-chatbot
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory with the following (fill in your actual values):

```env
AZURE_OPENAI_ENDPOINT=https://<your-endpoint>.openai.azure.com
AZURE_OPENAI_KEY=<your-key>
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
AZURE_OPENAI_API_VERSION=2024-02-15-preview

DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=docchat
```

### 4. Set up PostgreSQL (for Excel/CSV support)

- Install PostgreSQL and create a database named `docchat`
- Update `.env` with your DB credentials

---

## 5. ChromaDB Setup

ChromaDB is used as the vector database for storing and searching document embeddings.

- **No manual setup is required for local development.**  
  The database files will be created automatically in the `chroma_db/` directory when you run the app for the first time.

---

## Usage

### 1. Start the Streamlit UI

```sh
streamlit run app/ui/streamlit_app.py
```

### 2. Upload a document

- Use the web interface to upload a PDF, Excel, or CSV file.

### 3. Ask questions

- Type your question in the chat box.
- For PDFs, the bot uses semantic search and GPT to answer.
- For Excel/CSV, the bot uses a SQL agent to generate and run SQL queries on your data.

---

## Project Structure

```
app/
  agent/         # Chatbot and SQL agent logic
  config/        # LLM and settings configuration
  db/            # Database utilities
  ingestion/     # Document loaders and processors
  ui/            # Streamlit UI
  utils/         # Utility functions
  vectorstore/   # Vector DB logic
chroma_db/       # ChromaDB storage
temp/            # Temporary file storage
requirements.txt
.env
README.md
```

---

## Notes

- Make sure your Azure OpenAI deployment is active and the deployment name matches your `.env`.
- For large Excel files, only the schema (column names/types) is sent to the LLM to avoid context length errors.
- Uploaded files are processed and then deleted from the `temp/` directory.

---

## Troubleshooting

- **DeploymentNotFound**: Check your Azure OpenAI deployment name and endpoint.
- **Token/context length exceeded**: The table schema is too large; reduce the number of columns or rows.
- **Database errors**: Ensure PostgreSQL is running and credentials are correct.

---

## Credits

Built with [Streamlit](https://streamlit.io/), [ChromaDB](https://www.trychroma.com/), [LangChain](https://www.langchain.com/), and [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service).