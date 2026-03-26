from langgraph.graph import StateGraph
from langchain_ollama import OllamaLLM   # ✅ UPDATED

from app.agents.analyzer import analyzer_node
from app.agents.fixer import fixer_node
from app.agents.reporter import reporter_node


def build_graph(retriever):

    # ✅ Use latest Ollama LLM
    llm = OllamaLLM(model="mistral")

    # ✅ FIXED retrieval function
    def retrieve(state):
        docs = retriever.invoke(state["query"])   # 🔥 FIX

        context = "\n".join([doc.page_content for doc in docs])

        return {"context": context}

    # ✅ Create graph
    graph = StateGraph(dict)

    # Nodes
    graph.add_node("retrieve", retrieve)
    graph.add_node("analyze", lambda s: analyzer_node(s, llm))
    graph.add_node("fix", lambda s: fixer_node(s, llm))
    graph.add_node("report", lambda s: reporter_node(s, llm))

    # Flow
    graph.set_entry_point("retrieve")

    graph.add_edge("retrieve", "analyze")
    graph.add_edge("analyze", "fix")
    graph.add_edge("fix", "report")

    graph.set_finish_point("report")

    return graph.compile()