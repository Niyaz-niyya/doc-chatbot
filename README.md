# doc-chatbot

A document-based chatbot that allows users to upload PDF or Excel files, stores their content in a vector database or SQL database, and answers user queries using Azure OpenAI or Google Gemini and semantic search.

---

## Features

- Upload PDF, Excel, or CSV files via a web UI (Streamlit)
- PDF/Excel content is chunked and stored in a vector database (ChromaDB) or PostgreSQL (for structured data)
- Natural language queries are answered using **Azure OpenAI (GPT)** or **Google Gemini** and semantic search or SQL agent
- Supports both unstructured (PDF) and structured (Excel/CSV) data
- Modern chat interface with history
- **Flexible LLM provider selection** - Switch between Azure OpenAI and Google Gemini

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
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://<your-endpoint>.openai.azure.com
AZURE_OPENAI_KEY=<your-key>
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Google Gemini Configuration
GOOGLE_API_KEY=<your-google-api-key>
GEMINI_MODEL=gemini-2.0-flash-exp

# Choose LLM provider: "azure" or "gemini"
LLM_PROVIDER=gemini

# Database Configuration
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=docchat
```

### 4. Set up PostgreSQL (for Excel/CSV support)

- Install PostgreSQL and create a database named `docchat`
- Update `.env` with your DB credentials

### 5. LLM Provider Setup

#### Option A: Azure OpenAI
1. Create an Azure OpenAI resource in Azure Portal
2. Deploy a model (e.g., gpt-35-turbo)
3. Get your endpoint, API key, and deployment name
4. Set `LLM_PROVIDER=azure` in your `.env` file

#### Option B: Google Gemini
1. Get a Google AI Studio API key from [Google AI Studio](https://aistudio.google.com/)
2. Choose your preferred Gemini model (e.g., `gemini-2.0-flash-exp`)
3. Set `LLM_PROVIDER=gemini` in your `.env` file

---

## 6. ChromaDB Setup

ChromaDB is used as the vector database for storing and searching document embeddings.

- **No manual setup is required for local development.**  
  The database files will be created automatically in the `chroma_db/` directory when you run the app for the first time.
- **Do NOT commit the `chroma_db/` folder to git.**  
  Add `chroma_db/` to your `.gitignore` file.

If you want to start with a fresh database, simply delete the `chroma_db/` folder before running the app.

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
- For PDFs, the bot uses semantic search and your chosen LLM to answer.
- For Excel/CSV, the bot uses a SQL agent to generate and run SQL queries on your data.

### 4. Switch LLM Providers

To switch between Azure OpenAI and Google Gemini:
1. Update the `LLM_PROVIDER` variable in your `.env` file
2. Restart the application
3. The chatbot will automatically use the selected provider

---

## Project Structure

```
app/
  agent/         # Chatbot and SQL agent logic
  config/        # LLM and settings configuration
    llm.py       # Main LLM client factory
    gemini_llm.py # Google Gemini wrapper
    settings.py  # Environment variables
  db/            # Database utilities
  ingestion/     # Document loaders and processors
  ui/            # Streamlit UI
  utils/         # Utility functions
  vectorstore/   # Vector DB logic
chroma_db/       # ChromaDB storage (auto-generated)
temp/            # Temporary file storage
requirements.txt
.env
README.md
```

---

## Notes

- **LLM Provider**: You can switch between Azure OpenAI and Google Gemini by changing the `LLM_PROVIDER` environment variable.
- **Azure OpenAI**: Make sure your deployment is active and the deployment name matches your `.env`.
- **Google Gemini**: Ensure you have a valid API key from Google AI Studio.
- **Large Excel files**: Only the schema (column names/types) is sent to the LLM to avoid context length errors.
- **File cleanup**: Uploaded files are processed and then deleted from the `temp/` directory.

---

## Troubleshooting

### Common Issues

- **DeploymentNotFound (Azure)**: Check your Azure OpenAI deployment name and endpoint.
- **Invalid API Key (Gemini)**: Verify your Google AI Studio API key is correct and active.
- **Token/context length exceeded**: The table schema is too large; reduce the number of columns or rows.
- **Database errors**: Ensure PostgreSQL is running and credentials are correct.
- **LLM switching**: Restart the application after changing `LLM_PROVIDER` in `.env`.

### Testing LLM Connection

You can test your LLM connection by running:

```sh
python app/test_gemini.py  # For Gemini
```

---

## Credits

Built with [Streamlit](https://streamlit.io/), [ChromaDB](https://www.trychroma.com/), [LangChain](https://www.langchain.com/), [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service), and [Google Gemini](https://ai.google.dev/).