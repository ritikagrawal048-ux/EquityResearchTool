# 📈 Equity Research Analysis using RAG & Gemini

An AI-powered **Equity Research Assistant** built using **Retrieval-Augmented Generation (RAG)** and **Google Gemini**. The application ingests financial news and research article URLs, creates a vector-based knowledge base, and allows users to ask natural language questions. Answers are generated using relevant retrieved context and include source references for transparency.

---

## 🚀 Features

- 🔗 Load multiple financial news/article URLs
- 📄 Automatic content extraction and preprocessing
- ✂️ Intelligent document chunking
- 🧠 Semantic search using FAISS
- 🤖 Google Gemini-powered question answering
- 📚 Source attribution with every response
- ⚡ Interactive Streamlit web interface

---

## 🏗️ Project Architecture

```
User URLs
     │
     ▼
Load & Extract Articles
     │
     ▼
Text Splitting
     │
     ▼
Generate Embeddings
     │
     ▼
FAISS Vector Database
     │
     ▼
Similarity Search
     │
     ▼
Google Gemini LLM
     │
     ▼
Answer + Source References
```

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/EquityResearchAnalysis.git

cd EquityResearchAnalysis
```


install the following packages

```bash
pip3 install langchain
pip3 install langchain_community
pip3 install langchain_classic
pip3 install unstructured
pip3 install libmagic
pip3 install python-magic
pip3 install python-magic-bin
pip3 install faiss-cpu
#Add gemini key at env file
```

---

# ▶️ Run the Application

```bash
streamlit run main.py
```

The application will open in your default browser.

---

# 📚 Libraries Used

| Library | Purpose |
|----------|---------|
| **streamlit** | Creates the interactive web interface. |
| **langchain** | Provides the core framework for building the RAG pipeline. |
| **langchain-community** | Community integrations such as document loaders and vector stores. |
| **langchain-classic** | Supports classic LangChain components used by the project. |
| **langchain-google-genai** | Integrates Google Gemini models with LangChain. |
| **google-generativeai** | Official Google Gemini SDK for generating responses. |
| **FAISS (faiss-cpu)** | High-performance vector database for semantic similarity search. |
| **unstructured** | Extracts clean text from web pages and documents. |
| **libmagic** | Detects file types required by document loaders. |
| **python-magic** | Python wrapper around libmagic for file type detection. |
| **python-magic-bin** | Windows-compatible binary distribution of python-magic. |
| **python-dotenv** | Loads API keys and environment variables from a `.env` file. |

---

# ⚙️ How It Works

### 1. Article Ingestion

Users provide one or more financial article URLs.

### 2. Content Extraction

The application extracts textual content from the articles.

### 3. Text Chunking

Large documents are split into smaller chunks for efficient retrieval.

### 4. Embedding Generation

Each chunk is converted into vector embeddings.

### 5. Vector Storage

Embeddings are stored in a FAISS vector database.

### 6. Retrieval

When a question is asked, the most relevant document chunks are retrieved using semantic similarity search.

### 7. Response Generation

Google Gemini receives the retrieved context and generates an accurate answer grounded in the source documents.

### 8. Source Attribution

The application returns the answer along with references to the original articles.

---

# 🛠️ Tech Stack

- Python
- Google Gemini
- LangChain
- FAISS
- Streamlit
- Retrieval-Augmented Generation (RAG)

---

# 📁 Project Structure

```
EquityResearchAnalysis/
│
├── main.py
├── requirements.txt
├── .env
├── concept_notebooks/
├── faiss_index/
└── README.md
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

# 💡 Future Enhancements

- Support PDF annual reports
- Chat history
- Multi-document summarization
- Financial statement analysis
- Hybrid search (Keyword + Semantic)
- Persistent vector database

---

## ⭐ If you found this project useful, consider giving it a star!
