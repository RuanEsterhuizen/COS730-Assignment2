import sqlite3
import json

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_name = "app.db"
            cls._instance._init_db()
        return cls._instance

    
    def _init_db(self) -> None:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # reviewers table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviewers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            research_group TEXT
        )
        """)

        # submissions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            date TEXT,
            research_group TEXT,
            supervisor TEXT,
            abstract TEXT,
            keywords TEXT,
            scores TEXT
        )
        """)

        conn.commit()
        conn.close()

    def saveSubmission(self, data) -> tuple[bool,int]:
        print("DB: Saving submission")

        conn = None

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO submissions
                (
                    title,
                    author,
                    date,
                    research_group,
                    supervisor,
                    abstract,
                    keywords,
                    scores
                )
                VALUES (?,?,?,?,?,?,?,?)
                """,
                (
                    data["title"],
                    data["author"],
                    data["date"],
                    data["group"],
                    data["supervisor"],
                    data["abstract"],
                    data["keyword"],
                    json.dumps([])
                )
            )

            conn.commit()
            return True, cursor.lastrowid
        
        except Exception as e:
            print("DB Error:", e)
            return False
        
        finally:
            if conn:
                conn.close()

    def fetchReviewers(self) -> list:
        print("DB: Fetching reviewers")

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM reviewers")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            return [dict(zip(columns, row)) for row in rows]
        
        except Exception as e:
            print("DB Error:", e)
            return []
        
        finally:
            if conn:
                conn.close()

    def saveScores(self, submissionId:int, scores:list[int]) -> None:
        print("DB: Saving scores")

        conn = None

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE submissions
                SET scores=?
                WHERE id=?
                """,
                (
                    json.dumps(scores),
                    submissionId
                )
            )

            conn.commit()

        except Exception as e:
            print("DB Error:", e)

        finally:
            if conn:
                conn.close()

    def fetchScores(self, submissionId:int) -> list[int]:
        print("DB: Fetching Scores")
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute("SELECT scores FROM submissions WHERE id=?", (submissionId,))

            row = cursor.fetchone()
            scores = json.loads(row[0])

            return [int(score) for score in scores]

        except Exception as e:
            print("DB Error:", e)

        finally:
            if conn:
                conn.close()