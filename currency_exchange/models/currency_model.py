from .database import get_connection

class CurrencyModel:
    @staticmethod
    def all():
        with get_connection() as conn:
            return conn.execute("SELECT * FROM Currencies").fetchall()

    @staticmethod
    def get_by_code(code):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM Currencies WHERE Code=?", (code,)).fetchone()

    @staticmethod
    def insert(full_name, code, sign):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO Currencies (FullName, Code, Sign) VALUES (?, ?, ?)",
                        (full_name, code, sign))
            conn.commit()
            return cur.lastrowid
