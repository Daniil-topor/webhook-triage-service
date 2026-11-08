# Webhook Triage Service

Мини-сервис автоматической маршрутизации обращений. Принимает webhook, определяет категорию и приоритет, выбирает очередь и сохраняет объяснимое решение в SQLite.

## Возможности

- FastAPI и автоматическая документация OpenAPI;
- идемпотентная обработка по внешнему ID;
- категории billing, security, bug, feature и general;
- приоритеты от normal до critical;
- журнал решений и причины классификации;
- Docker и автоматические тесты.

## Запуск

```bash
docker build -t webhook-triage .
docker run --rm -p 8000:8000 webhook-triage
```

Документация API: [http://localhost:8000/docs](http://localhost:8000/docs)

Пример запроса:

```bash
curl -X POST http://localhost:8000/webhooks/tickets \
  -H "Content-Type: application/json" \
  -d '{"id":"demo-1","subject":"Срочно: оплата","message":"Деньги списали дважды"}'
```

## Тесты

```bash
python -m unittest discover -s tests -v
```
