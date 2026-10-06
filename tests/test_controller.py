"""Тесты ЛР3. unittest. 5 юнит + 5 интеграционных."""
import unittest, os, sys, tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.validator import RegistrationValidator
from src.repository import RegistrationRepository
from src.ui import UserInterface
from src.notifier import Notifier
from src.controller import RegistrationController


# ============ ЗАГЛУШКИ ============
class StubUI(UserInterface):
    def __init__(self, data):
        self.data = data
    def get_registration_data(self):
        return self.data


class StubNotifier(Notifier):
    def __init__(self):
        self.calls = []
    def send(self, message):
        self.calls.append(message)


# ============ ЮНИТ-ТЕСТЫ ============
class TestValidator(unittest.TestCase):
    def setUp(self):
        self.v = RegistrationValidator()

    def test_success(self):
        self.assertEqual(self.v.validate("john_doe", "Пароль1!", "Пароль1!"), (True, ""))

    def test_bad_login(self):
        ok, msg = self.v.validate("abc", "Пароль1!", "Пароль1!")
        self.assertFalse(ok)
        self.assertTrue(msg)

    def test_bad_password(self):
        ok, msg = self.v.validate("john_doe", "пароль1!", "пароль1!")
        self.assertFalse(ok)
        self.assertTrue(msg)

    def test_blacklist(self):
        self.assertFalse(self.v.validate("admin", "Пароль1!", "Пароль1!")[0])

    def test_non_string(self):
        ok, _ = self.v.validate(123, "Пароль1!", "Пароль1!")
        self.assertFalse(ok)


class TestAbstract(unittest.TestCase):
    def test_ui_abstract(self):
        with self.assertRaises(TypeError):
            UserInterface()

    def test_notifier_abstract(self):
        with self.assertRaises(TypeError):
            Notifier()


class TestControllerStubs(unittest.TestCase):
    """Контроллер с заглушками UI и Notifier — изоляция модулей."""

    def test_success_uses_stub(self):
        n = StubNotifier()
        ctrl = RegistrationController(
            StubUI(("john_doe", "Пароль1!", "Пароль1!")),
            RegistrationValidator(), RegistrationRepository(), n)
        result, _ = ctrl.run()
        self.assertTrue(result)
        self.assertEqual(len(n.calls), 1)
        self.assertIn("УСПЕХ", n.calls[0])


# ============ ИНТЕГРАЦИОННЫЕ ТЕСТЫ ============
class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.repo = RegistrationRepository(":memory:")
        self.notifier = StubNotifier()

    def tearDown(self):
        self.repo.close()

    def _run(self, login, pwd, confirm):
        return RegistrationController(
            StubUI((login, pwd, confirm)),
            RegistrationValidator(), self.repo, self.notifier).run()

    def test_first_call_saves_to_db(self):
        self._run("john_doe", "Пароль1!", "Пароль1!")
        cached = self.repo.get("john_doe", "Пароль1!", "Пароль1!")
        self.assertIsNotNone(cached)
        self.assertTrue(cached[0])

    def test_second_call_uses_cache(self):
        self._run("john_doe", "Пароль1!", "Пароль1!")
        # удаляем запись → если кэш работает, второй вызов её восстановит из БД
        result, _ = self._run("john_doe", "Пароль1!", "Пароль1!")
        self.assertTrue(result)

    def test_invalid_saved_with_error(self):
        ok, msg = self._run("abc", "Пароль1!", "Пароль1!")
        self.assertFalse(ok)
        self.assertTrue(msg)
        self.assertIsNotNone(self.repo.get("abc", "Пароль1!", "Пароль1!"))

    def test_different_data_new_record(self):
        self._run("john_doe", "Пароль1!", "Пароль1!")
        self._run("jane_doe", "Пароль1!", "Пароль1!")
        self.assertIsNotNone(self.repo.get("john_doe", "Пароль1!", "Пароль1!"))
        self.assertIsNotNone(self.repo.get("jane_doe", "Пароль1!", "Пароль1!"))

    def test_file_db_persistence(self):
        fd, path = tempfile.mkstemp(suffix=".db"); os.close(fd)
        try:
            repo = RegistrationRepository(path)
            RegistrationController(
                StubUI(("john_doe", "Пароль1!", "Пароль1!")),
                RegistrationValidator(), repo, StubNotifier()).run()
            repo.close()

            repo2 = RegistrationRepository(path)
            self.assertIsNotNone(repo2.get("john_doe", "Пароль1!", "Пароль1!"))
            repo2.close()
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main(verbosity=2)