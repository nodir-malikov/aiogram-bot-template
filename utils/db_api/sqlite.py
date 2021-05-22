import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE users(
            id integer PRIMARY KEY AUTOINCREMENT,
            chat_id varchar(255) NOT NULL,
            full_name varchar(255) NOT NULL,
            username varchar(255) NULL,
            lang varchar(2) NULL
            );"""

        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def new_user(self, chat_id, full_name, username):

        sql = """
        INSERT INTO users(chat_id, full_name, username) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(chat_id, full_name, username), commit=True)

    def set_language(self, chat_id, lang):

        sql = f"""
        UPDATE users SET lang = '{lang}' WHERE chat_id = {chat_id}
        """
        print(sql)
        self.execute(sql, commit=True)

    def get_user(self, chat_id):
        sql = f"""
        SELECT * FROM users WHERE chat_id = {chat_id}
        """
        result = self.execute(sql, fetchone=True)
        return result

    def get_all_users(self):
        sql = f"""
        SELECT * FROM users
        """
        result = self.execute(sql, fetchall=True)
        return result

    def count_all(self):
        sql = f"""
        SELECT COUNT(*) FROM users;
        """
        result = self.execute(sql, fetchall=True)
        return result[0][0]

    def get_lang(self, chat_id):
        # Делаем запрос к базе, узнаем установленный язык
        sql = f"""
        SELECT * FROM users WHERE chat_id = {chat_id}
        """
        result = self.execute(sql, fetchone=True)
        if result:
            return result[-1]
            # Если пользователь найден - возвращаем его код языка
        else:
            return None


def logger(statement):
    pass
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")
