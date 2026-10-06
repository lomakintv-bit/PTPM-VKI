from src.validator import RegistrationValidator
from src.repository import RegistrationRepository
from src.ui import ConsoleUserInterface
from src.notifier import EmailNotifier
from src.controller import RegistrationController

if __name__ == "__main__":
    ctrl = RegistrationController(
        ConsoleUserInterface(), RegistrationValidator(),
        RegistrationRepository("registrations.db"), EmailNotifier())
    print(ctrl.run())