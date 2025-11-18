from app.extractors.syllabus_extractor import SyllabusExtractor
from typing import Dict, Any, List, Optional

class LLMService:
    def __init__(self, extractor: SyllabusExtractor):
        self.kb = extractor.knowledge_base

    def generate_answer(self, user_query: str, intent: str, context: List[str]) -> str:
        kb = self.kb
        res = kb.get("Learning Resources", {})

        if intent == "SubjectDetails": return f"Subject Name: {kb.get('Subject Name')}"
        if intent == "CourseCode": return f"Course Code: {kb.get('Course Code')}"
        if intent == "Credits": return f"Credits: {kb.get('Credits')}"
        if intent == "Category": return f"Category: {kb.get('Category')}"

        if intent == "MarksCIA": return f"CIA Marks: {kb.get('CIA Marks')}"
        if intent == "MarksExternal": return f"External Marks: {kb.get('External Marks')}"
        if intent == "MarksTotal": return f"Total Marks: {kb.get('Total Marks')}"

        if intent == "MarksGeneral":
            return (
                f"CIA: {kb.get('CIA Marks')}\n"
                f"External: {kb.get('External Marks')}\n"
                f"Total: {kb.get('Total Marks')}"
            )

        if intent == "CourseOutcomes":
            outcomes = kb.get("Course Outcomes")
            if not outcomes:
                return "Course Outcomes not found."
            return "\n".join([f"- {co['CO']}: {co['Description']}" for co in outcomes])

        if intent == "UnitDetails":
            units = kb.get("Unit Details")
            if not units:
                return "Unit details not found."
            return "\n".join([f"- {u['Unit']}: {u['Content']}" for u in units])

        if intent == "Objectives":
            return kb.get("Overall Course Objectives")

        if intent == "Evaluation":
            return (
                f"Internal: {kb.get('Evaluation (Internal)')}\n"
                f"External: {kb.get('Evaluation (External)')}"
            )

        if intent == "TextBooks":
            books = res.get("TEXT BOOKS", [])
            if not books: return "No TEXT BOOKS found."
            return "\n".join([f"- {b}" for b in books])

        if intent == "ReferenceBooks":
            books = res.get("Reference Books", [])
            if not books: return "No Reference Books found."
            return "\n".join([f"- {b}" for b in books])

        if intent == "WebResources":
            urls = res.get("Web Resources", [])
            if not urls: return "No Web Resources found."
            return "\n".join([f"- {u}" for u in urls])

        if intent == "LearningResourcesGeneral":
            return (
                "**TEXT BOOKS**\n" + "\n".join(res.get("TEXT BOOKS", [])) + "\n\n" +
                "**Reference Books**\n" + "\n".join(res.get("Reference Books", [])) + "\n\n" +
                "**Web Resources**\n" + "\n".join(res.get("Web Resources", []))
            )

        if intent == "FallbackSearch" and context:
            return context[0]

        return f"No answer found for query: {user_query}"

