from fastapi import APIRouter, UploadFile, File
from app.utils.pdf_utils import extract_text_from_pdf
from app.extractors.syllabus_extractor import SyllabusExtractor
from app.storage.pkl_storage_manager import save_syllabus
import tempfile

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Save PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        text = extract_text_from_pdf(tmp_path)

        extractor = SyllabusExtractor(text)
        save_syllabus({
            "document": text,
            "kb": extractor.knowledge_base
        })

        return {
            "message": "PDF uploaded & syllabus saved successfully.",
            "filename": file.filename
        }

    except Exception as e:
        return {"error": str(e)}
