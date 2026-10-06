"""Отправка результата: абстрактный интерфейс + имитация."""
from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...


class EmailNotifier(Notifier):
    """Имитация email-сервера: сохраняет отправленное и печатает."""

    def __init__(self):
        self.sent = []

    def send(self, message):
        self.sent.append(message)
        print(f"[EMAIL] {message}")