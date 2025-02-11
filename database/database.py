import sqlite3
from datetime import datetime, timedelta
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
                answer TEXT UNIQUE,
                link TEXT,
                study TEXT,
                hour TEXT
            )
        ''')
        conn.commit()
        conn.close()


    def is_answer_in_db(self, answer):
        """
        Check if the given answer is already in the `scraped_answers` table.
        Returns True if the answer exists, otherwise False.
        """
        # Calculate the current date and time for the 'hour' field.
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM scraped_answers WHERE answer = ?', (answer,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def save_answer_to_db(self, answer, link, study):
        """
        Save the given answer to the `scraped_answers` table.
        """
        hour = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
        '''
        INSERT OR IGNORE INTO scraped_answers (answer, link, study, hour)
        VALUES (?, ?, ?, ?)
        ''',
        (answer, link, study, hour)
        )
        conn.commit()
        conn.close()
    def count_studies_since_yesterday(self):
        """
        Returns the number of studies in the 'scraped_answers' table
        that have a timestamp (in the 'hour' column) on or after yesterday's date.
        
        Assumes that the 'hour' column is stored as a string in the format 'YYYY-MM-DD HH:MM:SS'.
        """
        # Compute yesterday's date at midnight
        yesterday = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_str = yesterday.strftime('%Y-%m-%d %H:%M:%S')
        
        # Connect to the database and run the query
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # The query counts rows with a timestamp on or after yesterday's date.
        cursor.execute("SELECT COUNT(*) FROM scraped_answers WHERE hour >= ?", (yesterday_str,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    def get_studies_since_yesterday(self):
        """
        Returns a list of studies from the 'scraped_answers' table that have a timestamp (in the 'hour' column)
        on or after yesterday's date (starting at midnight).
        
        Each study is returned as a dictionary, where the keys are the column names.
        """
        # Calculate yesterday's date at midnight
        yesterday = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_str = yesterday.strftime('%Y-%m-%d %H:%M:%S')
        
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_name)
        # Enable dictionary-like access to rows
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Execute the query to fetch all studies since yesterday
        cursor.execute("SELECT * FROM scraped_answers WHERE hour >= ?", (yesterday_str,))
        rows = cursor.fetchall()
        
        # Close the connection
        conn.close()
        
        # Convert rows (sqlite3.Row objects) to a list of dictionaries
        studies = [dict(row) for row in rows]
        return studies
    
    def get_study_group_counts(self):
        """
        Returns a list of dictionaries, where each dictionary represents a study group
        and its count, grouped by the 'study' column.
        
        Example output:
        [
            {"study": "User Interviews", "count": 5},
            {"study": "Another Study", "count": 3},
            ...
        ]
        """
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name.
        cursor = conn.cursor()
        
        query = "SELECT study, COUNT(*) as count FROM scraped_answers GROUP BY study"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        # Convert each row to a dictionary.
        groups = [dict(row) for row in rows]
        return groups
