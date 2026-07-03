import os
import streamlit as st
import time
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_classic.chains import RetrievalQAWithSourcesChain
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# Set Google API key
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

st.title("RockyBot: News Research Tool 📈")
st.sidebar.title("News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")

# Define directory name for FAISS instead of a .pkl filename
folder_path = "faiss_store"

main_placeholder = st.empty()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.9,
    max_output_tokens=500
)

# Initialize embeddings once so it is accessible during both save and load phases
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    task_type="retrieval_document"
)

if process_url_clicked:
    # Load data
    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("Data Loading...Started...✅✅✅")
    data = loader.load()

    # Split data
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
    )
    main_placeholder.text("Text Splitter...Started...✅✅✅")
    docs = text_splitter.split_documents(data)

    # Create embeddings and save to FAISS index
    main_placeholder.text("Embedding Vector Started Building...✅✅✅")
    vectorstore_openai = FAISS.from_documents(docs, embeddings)
    time.sleep(2)

    # FIXED: Save the FAISS index using built-in local saving mechanisms instead of pickle
    vectorstore_openai.save_local(folder_path)
    main_placeholder.text("Vector Store Saved Locally!...🎉🎉🎉")

query = main_placeholder.text_input("Question: ")
if query:
    # FIXED: Check if the folder path exists
    if os.path.exists(folder_path):
        # FIXED: Load local FAISS database with embedding configuration and explicit deserialization permission
        vectorstore = FAISS.load_local(
            folder_path,
            embeddings,
            allow_dangerous_deserialization=True
        )

        chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
        result = chain({"question": query}, return_only_outputs=True)

        st.header("Answer")
        st.write(result["answer"])

        # Display sources, if available
        sources = result.get("sources", "")
        print("SOURCES ", sources)
        if sources:
            st.subheader("Sources:")
            sources_list = sources.split("\n")  # Split sources by newline
            for source in sources_list:
                st.write(source)
