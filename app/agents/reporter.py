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
        "analysis": state["analysis"],
        "fixes": state["fixes"]
    })

    return {"report": result}