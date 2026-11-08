from __future__ import annotations

from .models import TriageResult


CATEGORY_RULES = {
    "billing": ("оплата", "счет", "счёт", "возврат", "списали", "платеж"),
    "security": ("взлом", "утечка", "пароль", "подозритель", "доступ"),
    "bug": ("ошибка", "не работает", "сломал", "падает", "500", "баг"),
    "feature": ("добавьте", "хотелось бы", "функция", "возможность", "улучш"),
}

URGENT_MARKERS = ("срочно", "критично", "невозможно работать", "утечка", "взлом", "деньги списали")


def triage_ticket(subject: str, message: str) -> TriageResult:
    text = f"{subject} {message}".lower().replace("ё", "е")
    scores = {
        category: sum(1 for keyword in keywords if keyword.replace("ё", "е") in text)
        for category, keywords in CATEGORY_RULES.items()
    }
    category = max(scores, key=scores.get)
    best_score = scores[category]
    if best_score == 0:
        category = "general"

    urgent_hits = [marker for marker in URGENT_MARKERS if marker in text]
    if category == "security" or len(urgent_hits) >= 2:
        priority = "critical"
    elif urgent_hits or category == "billing":
        priority = "high"
    elif category == "bug":
        priority = "medium"
    else:
        priority = "normal"

    queue_map = {
        "billing": "finance-support",
        "security": "security-incident",
        "bug": "product-support",
        "feature": "product-discovery",
        "general": "customer-support",
    }
    reasons = [f"Совпадений категории: {best_score}"]
    if urgent_hits:
        reasons.append("Маркеры срочности: " + ", ".join(urgent_hits))
    confidence = min(0.95, 0.45 + best_score * 0.18 + len(urgent_hits) * 0.08)
    return TriageResult(category, priority, queue_map[category], round(confidence, 2), reasons)
