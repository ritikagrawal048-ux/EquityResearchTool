# 📄 Building a Production-Grade RAG Pipeline with Azure Document Intelligence & LangChain

When building enterprise Retrieval-Augmented Generation (RAG) applications, one of the biggest challenges is extracting **structured information** from PDFs.

Traditional PDF loaders often flatten documents into plain text, causing the loss of:

- 📊 Tables
- 📑 Headings
- 📍 Page Numbers
- 🖼️ Figures
- 📐 Reading Order
- 📄 Document Layout

This significantly reduces retrieval quality, especially for **financial reports, annual reports, research papers, invoices, and regulatory documents**.

A production-ready solution is to use **Azure Document Intelligence** (formerly Azure Form Recognizer) for document parsing and **LangChain** for building the RAG pipeline.

---

# 🏗️ Solution Architecture

```text
                           PDF Documents
                                │
                                ▼
               Azure Document Intelligence
                                │
      ┌───────────────┬───────────────┬──────────────┐
      │               │               │              │
 Paragraphs       Headings         Tables        Metadata
      │               │               │              │
      └───────────────┴───────────────┴──────────────┘
                                │
                                ▼
                  LangChain Document Objects
                                │
               Recursive Text Splitter
                                │
                                ▼
                        Generate Embeddings
                                │
                                ▼
             FAISS / Pinecone / Qdrant / Azure AI Search
                                │
                                ▼
                          Similarity Search
                                │
                                ▼
                         Google Gemini (LLM)
                                │
                                ▼
                  Accurate Answer + Source Citation
```

---

# 🚀 Step 1 — Install Required Packages

```bash
pip install azure-ai-documentintelligence
pip install langchain
pip install langchain-community
```

---

# 🔐 Step 2 — Create the Azure Document Intelligence Client

```python
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

client = DocumentIntelligenceClient(
    endpoint=AZURE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_KEY)
)
```

---

# 📑 Step 3 — Analyze the PDF

Use the **prebuilt-layout** model to preserve the complete document structure.

```python
with open("report.pdf", "rb") as f:

    poller = client.begin_analyze_document(
        "prebuilt-layout",
        body=f
    )

result = poller.result()
```

The Layout model extracts:

- Paragraphs
- Tables
- Headers
- Footers
- Figures
- Page Numbers
- Reading Order

---

# 📖 Step 4 — Extract Paragraphs

```python
paragraphs = []

for para in result.paragraphs:
    paragraphs.append(para.content)
```

Each paragraph can later be chunked and embedded independently.

---

# 📊 Step 5 — Extract Tables

Azure Document Intelligence reconstructs the table instead of flattening it.

```python
for table in result.tables:

    rows = table.row_count
    cols = table.column_count

    matrix = [["" for _ in range(cols)] for _ in range(rows)]

    for cell in table.cells:
        matrix[cell.row_index][cell.column_index] = cell.content

    print(matrix)
```

Instead of getting:

```
Revenue
100
Profit
20
```

You obtain structured data like:

| Quarter | Revenue | Profit |
|---------|----------|--------|
| Q1 | 100 | 20 |
| Q2 | 120 | 25 |

---

# 📝 Step 6 — Convert Tables to Markdown

LLMs understand Markdown tables significantly better than flattened text.

```python
import pandas as pd

df = pd.DataFrame(matrix)

markdown = df.to_markdown(index=False)
```

Result:

```markdown
| Quarter | Revenue | Profit |
|---------|----------|--------|
| Q1 |100|20|
| Q2 |120|25|
```

---

# 📄 Step 7 — Create LangChain Documents

Paragraphs:

```python
from langchain_core.documents import Document

docs = []

for para in result.paragraphs:

    docs.append(
        Document(
            page_content=para.content,
            metadata={
                "page": para.bounding_regions[0].page_number,
                "type": "paragraph"
            }
        )
    )
```

Tables:

```python
docs.append(
    Document(
        page_content=markdown,
        metadata={
            "page": page_number,
            "type": "table"
        }
    )
)
```

Metadata enables filtering during retrieval.

---

# ✂️ Step 8 — Chunk Only Paragraphs

Paragraphs are split into semantic chunks.

Tables should remain intact.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

paragraph_docs = splitter.split_documents(
    [d for d in docs if d.metadata["type"] == "paragraph"]
)
```

---

# 🧠 Step 9 — Generate Embeddings

```python
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004"
)
```

---

# 🗂️ Step 10 — Store in a Vector Database

```python
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(
    paragraph_docs + table_docs,
    embeddings
)
```

For production environments you may use:

- Pinecone
- Qdrant
- Weaviate
- Azure AI Search
- Milvus

instead of FAISS.

---

# 🚀 Production Best Practices

Instead of storing everything in one vector database, separate your content.

```text
                     Documents
                         │
        ┌────────────────┴───────────────┐
        │                                │
   Paragraph Chunks                 Tables
        │                                │
        ▼                                ▼
  Text Vector Index               Table Vector Index
        │                                │
        └───────────────┬────────────────┘
                        ▼
                 Query Classifier
                        ▼
                Retrieve Best Context
                        ▼
                   Gemini LLM
```

---

## 📊 Keep Tables Separate

Treat tables as structured knowledge rather than plain text.

Each table can be stored as:

```python
{
    "company": "Microsoft",
    "year": 2024,
    "page": 18,
    "section": "Income Statement",
    "type": "table"
}
```

This allows metadata filtering before retrieval.

---

## 🔍 Hybrid Retrieval

Production systems usually combine:

- Dense Vector Search
- BM25 Keyword Search

instead of relying on embeddings alone.

This dramatically improves retrieval quality.

---

## 🎯 Metadata Filtering

Instead of searching all documents:

```
100 PDFs
```

filter first:

```
Company = Apple

Year = 2024

Section = Income Statement
```

Then perform vector search.

This reduces latency and increases accuracy.

---

## 📈 Re-ranking

The retriever may return the Top 20 results.

A Cross Encoder or Gemini Re-ranker then selects the **Top 5** most relevant chunks before sending them to the LLM.

This is common in enterprise RAG systems.

---

## 📚 Source Attribution

Every answer should include:

- PDF Name
- Page Number
- Section
- Table Reference

Example:

```
Revenue increased by 12%.

Source:
Apple Annual Report 2024

Page 18

Income Statement
```

This builds user trust and improves explainability.

---

# 💡 Why Azure Document Intelligence?

Compared to traditional PDF loaders like **PyPDFLoader**, Azure Document Intelligence offers:

| Feature | Azure DI | Traditional PDF Loader |
|----------|-----------|------------------------|
| Paragraph Detection | ✅ | ⚠️ |
| Table Extraction | ✅ | ❌ |
| OCR Support | ✅ | ⚠️ |
| Reading Order | ✅ | ❌ |
| Figures | ✅ | ❌ |
| Layout Preservation | ✅ | ❌ |
| Page Numbers | ✅ | ⚠️ |

---

# 🎯 Final Takeaway

A production-grade RAG system should **never treat every PDF as plain text**.

Instead:

- ✅ Parse documents intelligently with Azure Document Intelligence
- ✅ Preserve tables and layout
- ✅ Convert tables into structured Markdown or JSON
- ✅ Build separate retrieval strategies for text and tables
- ✅ Use metadata filtering and hybrid search
- ✅ Re-rank retrieved chunks before passing them to the LLM
- ✅ Always return source citations

This architecture scales from **hundreds to thousands of documents** while delivering accurate, explainable, and enterprise-ready question answering.
