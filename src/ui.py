"""Ввод пользователя: абстрактный интерфейс + консольная реализация."""
from abc import ABC, abstractmethod


class UserInterface(ABC):
    @abstractmethod
    def get_registration_data(self): ...


class ConsoleUserInterface(UserInterface):
    def get_registration_data(self):
        return (input("Логин: ").strip(),
                input("Пароль: "),
                input("Подтверждение: "))