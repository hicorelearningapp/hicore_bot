class IntentClassifier:
    def classify(self, query: str) -> str:
        q = query.lower()

        if "subject name" in q or "course name" in q: return "SubjectDetails"
        if "course code" in q: return "CourseCode"
        if "credits" in q: return "Credits"
        if "category" in q: return "Category"

        if "cia" in q: return "MarksCIA"
        if "external marks" in q: return "MarksExternal"
        if "total marks" in q: return "MarksTotal"
        if "marks" in q: return "MarksGeneral"

        if "course outcomes" in q or "cos" in q: return "CourseOutcomes"
        if "unit details" in q or "syllabus" in q or "topics" in q: return "UnitDetails"
        if "objectives" in q: return "Objectives"
        if "evaluation" in q or "assessment" in q or "test" in q: return "Evaluation"

        # resource intents
        if "text book" in q: return "TextBooks"
        if "reference book" in q or "reference" in q: return "ReferenceBooks"
        if "web" in q or "url" in q: return "WebResources"
        if "resources" in q or "book" in q: return "LearningResourcesGeneral"

        return "FallbackSearch"