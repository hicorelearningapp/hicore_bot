from app.utils.pdf_utils import extract_text_from_pdf
from app.extractors.syllabus_extractor import SyllabusExtractor
from app.storage.pkl_storage_manager import load_all_syllabi, save_syllabus
from app.services.bot_service import BotService

class BotController:
    def __init__(self):
        self.syllabi = load_all_syllabi()
        self.bot = None

    def initialize(self):
        print(f"📚 Loaded {len(self.syllabi)} syllabi.")

        upload = input("Upload new PDF? (yes/no): ").strip().lower()
        if upload == "yes":
            path = input("Enter PDF path: ").strip()
            text = extract_text_from_pdf(path)
            extractor = SyllabusExtractor(text)
            save_syllabus({"document": text, "kb": extractor.knowledge_base})
            self.syllabi = load_all_syllabi()

        full_doc = ""
        full_kb = {}

        for s in self.syllabi:
            full_doc += s["document"]
            full_kb.update(s["kb"])

        final_extractor = SyllabusExtractor(full_doc)
        final_extractor.knowledge_base = full_kb

        self.bot = BotService(final_extractor, full_doc)
        print("🎓 Bot Ready with ALL syllabi!")

    def run(self):
        if not self.bot:
            print("Not initialized.")
            return

        while True:
            q = input("You: ")
            if q.lower() == "exit":
                break
            print("Bot:", self.bot.handle(q))
