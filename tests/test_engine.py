import tempfile
import unittest
from pathlib import Path

from triage import triage_ticket
from triage.storage import AuditStore


class TriageTests(unittest.TestCase):
    def test_routes_security_incident_as_critical(self):
        result = triage_ticket("Срочно: подозрительный доступ", "Похоже, аккаунт взломан")
        self.assertEqual(result.category, "security")
        self.assertEqual(result.priority, "critical")
        self.assertEqual(result.queue, "security-incident")

    def test_routes_payment_to_finance(self):
        result = triage_ticket("Оплата", "Деньги списали дважды")
        self.assertEqual(result.queue, "finance-support")
        self.assertEqual(result.priority, "high")

    def test_store_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            store = AuditStore(str(Path(directory) / "test.db"))
            result = triage_ticket("Ошибка", "Не работает кнопка")
            self.assertTrue(store.save("ticket-1", "Ошибка", result))
            self.assertFalse(store.save("ticket-1", "Ошибка", result))


if __name__ == "__main__":
    unittest.main()
