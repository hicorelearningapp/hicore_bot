from fastapi import APIRouter
from app.storage.pkl_storage_manager import load_all_syllabi
from app.extractors.syllabus_extractor import SyllabusExtractor
from app.services.bot_service import BotService

router = APIRouter()

@router.get("/ask")
def ask_question(q: str):
    syllabi = load_all_syllabi()

    if not syllabi:
        return {"error": "No syllabi available. Please upload PDFs first."}

    full_doc = ""
    full_kb = {}

    for s in syllabi:
        full_doc += s["document"] + "\n"
        full_kb.update(s["kb"])

    extractor = SyllabusExtractor(full_doc)
    extractor.knowledge_base = full_kb

    bot = BotService(extractor, full_doc)

    answer = bot.handle(q)

    return {
        "query": q,
        "answer": answer
    }
