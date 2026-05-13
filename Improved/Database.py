import sqlite3
import json

from Reviewer import Reviewer

class Database:
    def __init__(self, evaluationManager):
        self.db_name = "app.db"
        self.em = evaluationManager
        self._init_db()
    
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
            scores TEXT,
            reviewers TEXT
        )
        """)

        conn.commit()
        conn.close()

    def saveSubmission(self, data) -> bool:
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
                    scores,
                    reviewers
                )
                VALUES (?,?,?,?,?,?,?,?,?)
                """,
                (
                    data["title"],
                    data["author"],
                    data["date"],
                    data["group"],
                    data["supervisor"],
                    data["abstract"],
                    data["keyword"],
                    json.dumps([]),
                    json.dumps([])
                )
            )

            conn.commit()
            return True

        except Exception as e:
            print("DB Error:", e)
            return False

        finally:
            if conn:
                conn.close()

    def fetchReviewers(self) -> list[Reviewer]:
        print("DB: Fetching reviewers")

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM reviewers")
        rows = cursor.fetchall()

        return rows

    def _getSubmissionId(self, cursor, title:str):
        """
        Returns the most recently inserted submission
        matching the title.
        """

        cursor.execute(
            """
            SELECT id
            FROM submissions
            WHERE title=?
            ORDER BY id DESC
            LIMIT 1
            """,
            (title,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return row[0]

    def saveScore(self, title:str, score:int, reviewer:str) -> None:
        # TODO: this should get an array of scores and reviewer names
        print("DB: Saving score")

        conn = None

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            submission_id = self._getSubmissionId(cursor, title)

            if submission_id is None:
                print("Submission not found")
                return

            cursor.execute(
                "SELECT * FROM submissions WHERE id=?",
                (submission_id,)
            )

            row = cursor.fetchone()

            scores = json.loads(row[8]) if row[8] else []
            reviewers = json.loads(row[9]) if row[9] else []

            scores.append(score)
            reviewers.append(reviewer)

            new_scores = json.dumps(scores)
            new_reviewers = json.dumps(reviewers)

            cursor.execute(
                """
                UPDATE submissions
                SET scores=?, reviewers=?
                WHERE id=?
                """,
                (
                    new_scores,
                    new_reviewers,
                    submission_id
                )
            )

            conn.commit()

        except Exception as e:
            print("DB Error:", e)

        finally:
            if conn:
                conn.close()