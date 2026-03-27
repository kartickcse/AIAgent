from langchain_core.prompts import ChatPromptTemplate
def reporter_node(state, llm):
    prompt = ChatPromptTemplate.from_template("""
    Create an executive security report:

    Analysis:
    {analysis}

    Fixes:
    {fixes}
    """)

    chain = prompt | llm

    result = chain.invoke({
        "analysis": state.get("analysis", "No analysis found"),
        "fixes": state.get("fixes", "No fixes found")
    })

    # ✅ merge state
    return {**state, "report": result}