from dataclasses import asdict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from triage import triage_ticket
from triage.storage import AuditStore


app = FastAPI(
    title="Webhook Triage Service",
    description="Принимает обращения, объяснимо классифицирует их и маршрутизирует по очередям.",
    version="1.0.0",
)
store = AuditStore()


class Ticket(BaseModel):
    id: str = Field(min_length=1, max_length=100)
    subject: str = Field(min_length=1, max_length=300)
    message: str = Field(min_length=1, max_length=10_000)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/webhooks/tickets")
def receive_ticket(ticket: Ticket) -> dict:
    result = triage_ticket(ticket.subject, ticket.message)
    if not store.save(ticket.id, ticket.subject, result):
        raise HTTPException(409, "Ticket with this id was already processed")
    return {"ticket_id": ticket.id, **asdict(result)}


@app.get("/decisions")
def decisions(limit: int = 20) -> list[dict]:
    return store.recent(max(1, min(limit, 100)))
