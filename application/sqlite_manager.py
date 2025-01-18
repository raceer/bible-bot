import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file)
        self.cursor = self.db.cursor()

        self.create_tables()

    def create_tables(self):
        self.cursor.execute("BEGIN;")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Counters (
        chat_id INTEGER PRIMARY KEY,
        score INTEGER DEFAULT 0
        );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Timezones (
        chat_id INTEGER PRIMARY KEY,
        timezone STRING DEFAULT '0:00:00'
        );
        """)

        self.cursor.execute("COMMIT;")

    def add_user(self, chat_id, score = 0):
        self.cursor.execute("""
        INSERT OR IGNORE INTO Counters (chat_id) VALUES (?)""",
        [chat_id])

        self.cursor.execute("""
        INSERT OR IGNORE INTO Timezones (chat_id) VALUES (?)""",
        [chat_id])

    def get_score(self, chat_id):
        score = self.cursor.execute("""
        SELECT score
        FROM Counters
        WHERE chat_id = ?
        """,
        [chat_id]).fetchone()[0]
        return score

    def update_score(self, chat_id, score):
        self.cursor.execute("""
        UPDATE Counters SET score = ? WHERE chat_id = ?""",
        [score, chat_id])

        self.cursor.execute("COMMIT;")

    def tz_update(self, chat_id, tz):
        self.cursor.execute("""
        UPDATE Timezones SET timezone = ? WHERE chat_id = ?""",
        [tz, chat_id])

        self.cursor.execute("COMMIT;")

    def tz_get(self, chat_id):
        timezone = self.cursor.execute("""
        SELECT timezone
        FROM Timezones
        WHERE chat_id = ?
        """,
        [chat_id]).fetchone()[0]
        return timezone


if __name__ == "__main__":
    db = DatabaseManager("cache/user_data.db")
    user = 923283
    db.add_user(user)
    print(db.get_score(user))
