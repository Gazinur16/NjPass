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

    def add_pass_for_user(self, tg_id: int, name_pass: str, login: str, password: bytes, description: str):
        with self.connection:
            return self.cursor.execute("INSERT INTO `pass` (tg_id, name_pass, login, pass, description) "
                                       "VALUES (?,?,?,?,?)", (tg_id, name_pass, login, password, description))

    def get_name_pass_user(self, tg_id):
        with self.connection:
            return self.cursor.execute("SELECT id, name_pass FROM `pass` WHERE `tg_id` = ?", (tg_id,)).fetchall()

    def check_msr_key(self, tg_id):
        with self.connection:
            return self.cursor.execute("SELECT pass FROM `pass` WHERE `tg_id` = ?", (tg_id,)).fetchmany()

    def get_pass_user(self, id_pass: int):
        with self.connection:
            return self.cursor.execute("SELECT name_pass, login, pass, description FROM `pass` WHERE `id` = ?",
                                       (id_pass,)).fetchall()

    def del_pass_user(self, id_pass: int):
        with self.connection:
            self.cursor.execute("DELETE FROM `pass` WHERE `id` = ?", (id_pass,))

    def del_user(self, tg_id: int):
        with self.connection:
            self.cursor.execute("DELETE FROM `users` WHERE `tg_id` = ?", (tg_id,))
            self.cursor.execute("DELETE FROM `pass` WHERE `tg_id` = ?", (tg_id,))
