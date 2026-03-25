from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def create_agent(vector_db):
    llm = Ollama(model="mistral")

    retriever = vector_db.as_retriever()

    prompt = ChatPromptTemplate.from_template("""
    You are a cybersecurity expert.

    Context:
    {context}

    Question:
    {question}

    Answer clearly with:
    - Vulnerability
    - Severity
    - Fix
    """)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain