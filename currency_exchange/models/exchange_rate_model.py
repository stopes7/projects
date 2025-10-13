from .database import get_connection

class ExchangeRateModel:
    @staticmethod
    def all():
        with get_connection() as conn:
            return conn.execute("SELECT * FROM ExchangeRates").fetchall()

    @staticmethod
    def get(base_id, target_id):
        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM ExchangeRates WHERE BaseCurrencyId=? AND TargetCurrencyId=?",
                (base_id, target_id)
            ).fetchone()

    @staticmethod
    def insert(base_id, target_id, rate):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?, ?, ?)",
                (base_id, target_id, rate)
            )
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def update(base_id, target_id, rate):
        with get_connection() as conn:
            conn.execute(
                "UPDATE ExchangeRates SET Rate=? WHERE BaseCurrencyId=? AND TargetCurrencyId=?",
                (rate, base_id, target_id)
            )
            conn.commit()
