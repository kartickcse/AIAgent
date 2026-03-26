from langchain_core.prompts import ChatPromptTemplate

def fixer_node(state, llm):
    prompt = ChatPromptTemplate.from_template("""
    Based on the vulnerabilities below, suggest fixes:

    {analysis}
    """)

    chain = prompt | llm
    result = chain.invoke({"analysis": state["analysis"]})

    return {"fixes": result}