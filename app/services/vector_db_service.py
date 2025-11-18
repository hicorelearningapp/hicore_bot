from typing import Dict, Any, List, Optional
class VectorDatabaseService:
    def __init__(self, syllabus_document: str):
        self.document = syllabus_document

    def search(self, query: str, intent: str, kb: Dict[str, Any]) -> List[str]:
        if intent in [
            "SubjectDetails", "CourseCode", "Credits", "Category",
            "MarksCIA", "MarksExternal", "MarksTotal", "MarksGeneral",
            "Objectives", "Evaluation"
        ]:
            return [f"{key}: {kb.get(key)}"
                    for key in kb if intent.replace("Details", "").replace("Marks", "").lower() in key.lower()]

        if intent == "CourseOutcomes":
            return [f"CO: {co['Description']} | Mapping: {co['Mapping']}" for co in kb.get("Course Outcomes", [])]

        if intent == "UnitDetails":
            return [f"{u['Unit']}: {u['Content']}" for u in kb.get("Unit Details", [])]

        if intent == "TextBooks":
            return [str(kb.get("Learning Resources", {}).get("TEXT BOOKS"))]

        if intent == "ReferenceBooks":
            return [str(kb.get("Learning Resources", {}).get("Reference Books"))]

        if intent == "WebResources":
            return [str(kb.get("Learning Resources", {}).get("Web Resources"))]

        if intent == "LearningResourcesGeneral":
            res = kb.get("Learning Resources", {})
            return [
                f"TEXT BOOKS: {res.get('TEXT BOOKS')}",
                f"Reference Books: {res.get('Reference Books')}",
                f"Web Resources: {res.get('Web Resources')}",
            ]

        # fallback search in raw document
        if intent == "FallbackSearch":
            term = query.split()[-1]
            matches = [
                line.strip() for line in self.document.split("\n")
                if term.lower() in line.lower() and len(line) > 20
            ]
            return [f"Fallback Context: {matches[0]}"] if matches else ["No relevant context found."]

        return ["No relevant context found."]