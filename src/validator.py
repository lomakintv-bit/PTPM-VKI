"""Валидатор регистрации (ЛР1, обёрнутый в класс)."""
import re
import logging
import hashlib

logger = logging.getLogger("RegistrationValidator")
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    for h in (logging.FileHandler("registration.log", encoding="utf-8"),
              logging.StreamHandler()):
        h.setFormatter(fmt)
        logger.addHandler(h)


BLACKLIST = {"admin", "root", "user", "guest", "test", "qwerty", "system"}
PHONE = re.compile(r"^\+\d{1,3}-\d{3}-\d{3}-\d{4}$")
EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[A-Za-z]{2,}$")
LOGIN = re.compile(r"^[A-Za-z0-9_]{5,}$")
PWD_OK = re.compile(r"^[А-Яа-яЁё0-9!@#$%^&*()_\-+=<>.?/\\|{}\[\]~`\"':;,]+$")
UPPER = re.compile(r"[А-ЯЁ]")
LOWER = re.compile(r"[а-яё]")
DIGIT = re.compile(r"\d")
SPECIAL = re.compile(r"[!@#$%^&*()_\-+=<>.?/\\|{}\[\]~`\"':;,]")


def mask(password):
    if password is None:
        return "<None>"
    return f"***{hashlib.sha256(password.encode()).hexdigest()[:12]}***"


class RegistrationValidator:
    """Единственный публичный метод — validate(login, password, confirm) -> (bool, str)."""

    def validate(self, login, password, confirm):
        info = f"login={login!r}, password={mask(password)}"
        try:
            for name, value in (("login", login), ("password", password), ("confirm", confirm)):
                if value is not None and not isinstance(value, str):
                    return self._fail(info, f"Поле '{name}' должно быть строкой.")

            for ok, msg in (self._check_login(login), self._check_password(password, confirm)):
                if not ok:
                    return self._fail(info, msg)

            logger.info(f"OK | {info}")
            return True, ""

        except Exception as e:
            logger.exception(f"ERROR | {info} | {e}")
            return False, f"Внутренняя ошибка: {e}"

    @staticmethod
    def _fail(info, msg):
        logger.warning(f"FAIL | {info} | {msg}")
        return False, msg

    @staticmethod
    def _check_login(login):
        if not login or not login.strip():
            return False, "Логин не может быть пустым."
        login = login.strip()
        if len(login) > 100:
            return False, "Логин слишком длинный."
        if not (PHONE.match(login) or EMAIL.match(login) or LOGIN.match(login)):
            return False, "Некорректный формат логина."
        if login.lower() in BLACKLIST:
            return False, "Логин в чёрном списке."
        return True, ""

    @staticmethod
    def _check_password(password, confirm):
        if not password:
            return False, "Пароль не может быть пустым."
        if len(password) < 7:
            return False, "Пароль должен содержать минимум 7 символов."
        if not PWD_OK.match(password):
            return False, "Недопустимые символы в пароле."
        if not UPPER.search(password):
            return False, "Нужна заглавная буква."
        if not LOWER.search(password):
            return False, "Нужна строчная буква."
        if not DIGIT.search(password):
            return False, "Нужна цифра."
        if not SPECIAL.search(password):
            return False, "Нужен спецсимвол."
        if password != confirm:
            return False, "Пароль и подтверждение не совпадают."
        return True, ""