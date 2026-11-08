from dataclasses import dataclass


@dataclass(frozen=True)
class TriageResult:
    category: str
    priority: str
    queue: str
    confidence: float
    reasons: list[str]
