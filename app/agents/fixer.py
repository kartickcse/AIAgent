from langchain_core.prompts import ChatPromptTemplate
def fixer_node(state, llm):
    prompt = ChatPromptTemplate.from_template("""
    Suggest fixes for:

    {analysis}
    """)

    chain = prompt | llm
    result = chain.invoke({"analysis": state["analysis"]})

    # ✅ merge state
    return {**state, "fixes": result}