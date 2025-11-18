from typing import Dict, Any, List, Optional
class PromptBuilder:
    def build_prompt(self, user_query: str, intent: str, context: List[str]) -> str:
        return (
            f"You are a Syllabus RAG Bot.\n"
            f"User Query: {user_query}\n"
            f"Intent: {intent}\n"
            f"Context:\n" + "\n".join(context) + "\n"
            f"Answer strictly based on context."
        )
