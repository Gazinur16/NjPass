import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `tg_id` = ?", (tg_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, tg_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (tg_id) VALUES (?)", (tg_id,))

    def get_password_storage(self, tg_id):
        with self.connection:
            return self.cursor.execute("SELECT msr_key FROM `users` WHERE `tg_id` = ?", (tg_id,)).fetchall()
