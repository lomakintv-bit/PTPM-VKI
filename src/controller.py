"""Контроллер сквозного сценария."""
from src.validator import RegistrationValidator
from src.repository import RegistrationRepository
from src.ui import UserInterface
from src.notifier import Notifier


class RegistrationController:
    def __init__(self, ui: UserInterface, validator: RegistrationValidator,
                 repo: RegistrationRepository, notifier: Notifier):
        self.ui, self.validator, self.repo, self.notifier = ui, validator, repo, notifier

    def run(self):
        login, password, confirm = self.ui.get_registration_data()

        cached = self.repo.get(login, password, confirm)
        if cached is not None:
            result, message = cached
            source = "БД"
        else:
            result, message = self.validator.validate(login, password, confirm)
            self.repo.add(login, password, confirm, result, message)
            source = "вычисление"

        self.notifier.send(f"Результат: {result} | {message or 'УСПЕХ'} ({source})")
        return result, message