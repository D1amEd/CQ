import sqlite3

class Database:
    def __init__(self, db_name='scraped_data.db'):
        """
        Initialize the Database class with the name of the database file.
        It will initialize the database if it does not already exist.
        """
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """
        Create the database and the `scraped_answers` table if they do not exist.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraped_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                answer TEXT UNIQUE
            )
        ''')
        conn.commit()
        conn.close()

    def is_answer_in_db(self, answer):
        """
        Check if the given answer is already in the `scraped_answers` table.
        Returns True if the answer exists, otherwise False.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM scraped_answers WHERE answer = ?', (answer,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def save_answer_to_db(self, answer):
        """
        Save the given answer to the `scraped_answers` table.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO scraped_answers (answer) VALUES (?)', (answer,))
        conn.commit()
        conn.close()