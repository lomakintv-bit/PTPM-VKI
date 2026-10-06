"""Работа с SQLite."""
import sqlite3


class RegistrationRepository:
    def __init__(self, db_path=":memory:"):
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                login TEXT, password TEXT, confirm TEXT,
                result INTEGER, message TEXT,
                PRIMARY KEY (login, password, confirm))
        """)
        self._conn.commit()

    def add(self, login, password, confirm, result, message=""):
        self._conn.execute(
            "INSERT OR REPLACE INTO registrations VALUES (?, ?, ?, ?, ?)",
            (login, password, confirm, int(result), message))
        self._conn.commit()

    def get(self, login, password, confirm):
        row = self._conn.execute(
            "SELECT result, message FROM registrations "
            "WHERE login=? AND password=? AND confirm=?",
            (login, password, confirm)).fetchone()
        return (bool(row["result"]), row["message"] or "") if row else None

    def delete(self, login, password, confirm):
        self._conn.execute(
            "DELETE FROM registrations WHERE login=? AND password=? AND confirm=?",
            (login, password, confirm))
        self._conn.commit()

    def close(self):
        self._conn.close()