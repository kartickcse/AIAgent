
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS

# NEW ✅
from langchain_community.embeddings import OllamaEmbeddings

def create_vector_db(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    embeddings = OllamaEmbeddings(model="mistral")

    db = FAISS.from_texts(chunks, embeddings)
    return db