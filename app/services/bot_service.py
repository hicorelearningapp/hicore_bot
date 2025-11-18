class BotService:
    def __init__(self, extractor, document):
        from .analytics_service import AnalyticsService
        from .intent_classifier import IntentClassifier
        from .vector_db_service import VectorDatabaseService
        from .prompt_builder import PromptBuilder
        from .llm_service import LLMService

        self.analytics = AnalyticsService()
        self.intent_classifier = IntentClassifier()
        self.vector_db = VectorDatabaseService(document)
        self.prompt_builder = PromptBuilder()
        self.llm_service = LLMService(extractor)

    def handle(self, query: str) -> str:
        self.analytics.log(query)

        intent = self.intent_classifier.classify(query)
        context = self.vector_db.search(query, intent, self.llm_service.kb)
        response = self.llm_service.generate_answer(query, intent, context)

        return response
