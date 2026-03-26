from langchain_core.prompts import ChatPromptTemplate

def analyzer_node(state, llm):
    prompt = ChatPromptTemplate.from_template("""
    You are a cybersecurity expert.

    Analyze the context and extract:
    - Vulnerabilities
    - Severity
    - Impact

    Context:
    {context}
    """)

    chain = prompt | llm
    result = chain.invoke({"context": state["context"]})

    return {"analysis": result}