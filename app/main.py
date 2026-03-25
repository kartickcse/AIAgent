from fastapi import FastAPI, UploadFile, File
from app.logger import setup_logger
from app.pdf_loader import load_pdf
from app.rag import create_vector_db
from app.agent import create_agent

app = FastAPI()

logger = setup_logger()

agent = None

@app.get("/")
def home():
    return {"message": "DevSecAI API is running 🚀"}

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    global agent

    logger.info(f"Uploading file: {file.filename}")

    path = f"data/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    text = load_pdf(path)
    logger.info("PDF loaded successfully")

    db = create_vector_db(text)
    logger.info("Vector DB created")

    agent = create_agent(db)
    logger.info("Agent initialized")

    return {"status": "PDF processed"}


@app.get("/ask/")
def ask(query: str):
    logger.info(f"User query: {query}")

    try:
        response = agent.invoke(query)
        logger.info("Response generated successfully")
        return {"response": response}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {"error": str(e)}