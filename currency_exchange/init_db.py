import sqlite3

DB_FILE = "exchange.db"

currencies = [
    ("USD", "United States dollar", "$"),
    ("EUR", "Euro", "€"),
    ("RUB", "Russian ruble", "₽"),
    ("JPY", "Japanese yen", "¥"),
    ("AUD", "Australian dollar", "A$")
]

exchange_rates = [
    ("USD", "EUR", 0.93),
    ("EUR", "USD", 1.08),
    ("USD", "RUB", 95.0),
    ("RUB", "USD", 0.0105),
    ("USD", "JPY", 150.3),
    ("USD", "AUD", 1.55),
    ("AUD", "USD", 0.65)
]

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # Таблицы
    cur.executescript("""
    DROP TABLE IF EXISTS ExchangeRates;
    DROP TABLE IF EXISTS Currencies;

    CREATE TABLE Currencies (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Code TEXT UNIQUE NOT NULL,
        FullName TEXT NOT NULL,
        Sign TEXT NOT NULL
    );

    CREATE TABLE ExchangeRates (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        BaseCurrencyId INTEGER NOT NULL,
        TargetCurrencyId INTEGER NOT NULL,
        Rate REAL NOT NULL,
        UNIQUE(BaseCurrencyId, TargetCurrencyId),
        FOREIGN KEY(BaseCurrencyId) REFERENCES Currencies(ID),
        FOREIGN KEY(TargetCurrencyId) REFERENCES Currencies(ID)
    );
    """)

    # Добавляем валюты
    for code, name, sign in currencies:
        cur.execute("INSERT INTO Currencies (Code, FullName, Sign) VALUES (?, ?, ?)", (code, name, sign))

    # Добавляем курсы
    for base, target, rate in exchange_rates:
        cur.execute("SELECT ID FROM Currencies WHERE Code=?", (base,))
        base_id = cur.fetchone()[0]
        cur.execute("SELECT ID FROM Currencies WHERE Code=?", (target,))
        target_id = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?, ?, ?)",
            (base_id, target_id, rate)
        )

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_db()
