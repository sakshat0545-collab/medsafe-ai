class RiskEngine:
    def __init__(self):
        self.high_risk_keywords = [
            "chest pain", "unconscious", "severe bleeding",
            "difficulty breathing", "stroke", "heart attack"
        ]

        self.medium_risk_keywords = [
            "high fever", "persistent vomiting",
            "severe headache", "infection", "dehydration"
        ]

    def assess_risk(self, text):
        text = text.lower()

        for word in self.high_risk_keywords:
            if word in text:
                return {
                    "level": "HIGH",
                    "score": 90,
                    "color": "red"
                }

        for word in self.medium_risk_keywords:
            if word in text:
                return {
                    "level": "MEDIUM",
                    "score": 60,
                    "color": "orange"
                }

        return {
            "level": "LOW",
            "score": 30,
            "color": "green"
        }