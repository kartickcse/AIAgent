# from fastapi import FastAPI, UploadFile, File
# from app.logger import setup_logger
# from app.pdf_loader import load_pdf
# from app.rag import create_vector_db
# from app.agent import create_agent
# from app.agents.graph import build_graph

# graph = None

# app = FastAPI()

# logger = setup_logger()

# # agent = None

# @app.get("/")
# def home():
#     return {"message": "DevSecAI API is running 🚀"}

# @app.post("/upload/")
# async def upload(file: UploadFile = File(...)):
#     global agent

#     logger.info(f"Uploading file: {file.filename}")

#     path = f"data/{file.filename}"
#     with open(path, "wb") as f:
#         f.write(await file.read())

#     text = load_pdf(path)
#     logger.info("PDF loaded successfully")

#     db = create_vector_db(text)
#     logger.info("Vector DB created")

#     agent = create_agent(db)
#     logger.info("Agent initialized")
#      # ✅ SET GRAPH HERE
#     graph = build_graph(db.as_retriever())

#     logger.info("Graph initialized successfully")

#     return {"status": "PDF processed"}


# # @app.get("/ask/")
# # def ask(query: str):
# #     logger.info(f"User query: {query}")

# #     try:
# #         response = agent.invoke(query)
# #         logger.info("Response generated successfully")
# #         return {"response": response}
# #     except Exception as e:
# #         logger.error(f"Error: {str(e)}")
# #         return {"error": str(e)}
# @app.get("/ask/")
# def ask(query: str):
#     global graph

#     if app.state.graph is None:
#      return {"error": "Upload PDF first"}

#     result = app.state.graph.invoke(query)
#     logger.info(f"User query: {query}")
#     return {
#         "analysis": result["analysis"],
#         "fixes": result["fixes"],
#         "report": result["report"]
#     }
from fastapi import FastAPI, UploadFile, File
import os

from app.logger import setup_logger
from app.pdf_loader import load_pdf
from app.rag import create_vector_db
from app.agents.graph import build_graph

app = FastAPI()
app.state.graph = None

logger = setup_logger()

os.makedirs("data", exist_ok=True)


@app.get("/")
def home():
    return {"message": "DevSecAI API running 🚀"}


@app.post("/upload/")
async def upload(file: UploadFile = File(...)):

    logger.info(f"Uploading: {file.filename}")

    path = f"data/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    text = load_pdf(path)
    logger.info("PDF loaded")

    db = create_vector_db(text)
    logger.info("Vector DB created")

    app.state.graph = build_graph(db.as_retriever())
    logger.info("Graph ready")

    return {"status": "PDF processed"}


@app.get("/ask/")
def ask(query: str):

    logger.info("==== /ask API CALLED ====")
    logger.info(f"Incoming query: {query}")

    # 🔍 Check graph existence
    logger.info(f"Graph object: {app.state.graph}")

    if app.state.graph is None:
        logger.warning("Graph is None ❌ → Upload not done or state lost")
        return {"error": "Upload PDF first"}

    try:
        logger.info("Invoking LangGraph...")

        result = app.state.graph.invoke({"query": query})

        logger.info("Graph execution completed ✅")
        logger.info(f"Raw result: {result}")

        analysis = result.get("analysis")
        fixes = result.get("fixes")
        report = result.get("report")

        logger.info(f"Analysis: {analysis}")
        logger.info(f"Fixes: {fixes}")
        logger.info(f"Report: {report}")

        return {
            "analysis": analysis,
            "fixes": fixes,
            "report": report
        }

    except Exception as e:
        logger.error("❌ ERROR during graph execution")
        logger.error(str(e), exc_info=True)

        return {"error": str(e)}