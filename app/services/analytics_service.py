from datetime import datetime

class AnalyticsService:
    def log(self, query: str):
        print(f"[Analytics] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {query}")
