class IPODecisionAssistant:
    def __init__(self, responses):
        self.responses = responses
        self.score = 0

    def evaluate(self):
        questions = [
            ("Is the company profitable?", 5),
            ("Is the underwriter a top-tier bank (e.g., Goldman Sachs)?", 4),
            ("Are there strong pre-IPO investors (e.g., Sequoia)?", 4),
            ("Is the IPO price valuation reasonable compared to peers?", 5),
            ("Is the IPO oversubscribed 5x or more?", 3),
            ("Did you get IPO allocation?", 2),
            ("Is the open price less than 15% higher than the IPO price?", 2),
            ("Is the company in a growing sector with strong moat?", 5)
        ]
        for i, (q, weight) in enumerate(questions):
            if self.responses[i].lower() == 'y':
                self.score += weight

    def decision(self):
        if self.score >= 25:
            return "✅ Strong Buy: The IPO shows strong fundamentals."
        elif 15 <= self.score < 25:
            return "🔄 Moderate Buy: Consider investing with caution."
        elif 5 <= self.score < 15:
            return "⚠️ Risky: Consider avoiding unless you have a strategic reason."
        else:
            return "❌ Avoid: IPO doesn't meet hedge fund standards."

# 🔧 Example usage:
# Provide 'y' or 'n' for each of the 8 questions below
questions = [
    ("Is the company profitable?", 5),
    ("Is the underwriter a top-tier bank (e.g., Goldman Sachs)?", 4),
    ("Are there strong pre-IPO investors (e.g., Sequoia)?", 4),
    ("Is the IPO price valuation reasonable compared to peers?", 5),
    ("Is the IPO oversubscribed 5x or more?", 3),
    ("Did you get IPO allocation?", 2),
    ("Is the open price less than 15% higher than the IPO price?", 2),
    ("Is the company in a growing sector with strong moat?", 5)
]
your_responses = []
for q, _ in questions:
    response = input(f"{q} (y/n): ")
    your_responses.append(response)
assistant = IPODecisionAssistant(your_responses)
assistant.evaluate()
print(assistant.decision())
