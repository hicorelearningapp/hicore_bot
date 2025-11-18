from fastapi import FastAPI
from app.routers.uploads import router as uploads_router
from app.routers.ask import router as ask_router

app = FastAPI(
    title="Syllabus RAG Bot API",
    version="1.0"
)

app.include_router(uploads_router, prefix="/api")
app.include_router(ask_router, prefix="/api")

@app.get("/")
def home():
    return {"message": "Syllabus RAG Bot API is running!"}
