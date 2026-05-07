import sqlite3
import json

from Reviewer import Reviewer

class Database:
    def __init__(self):
        self.db_name = "app.db"
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
                (title, author, date, research_group, supervisor, abstract, keywords, scores, reviewers)
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

        reviewers = []

        for row in rows:
            reviewer = Reviewer(row[1], row[2])
            reviewers.append(reviewer)

        conn.close()

        return reviewers

    def saveScore(self, title:str, score:int, reviewer:str) -> None:
        print("DB: Saving score")

        conn = None

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM submissions WHERE title=?",
                (title,)
            )

            row = cursor.fetchone()

            if row is None:
                print("Submission not found")
                return

            scores = json.loads(row[8]) if row[8] else []
            reviewers = json.loads(row[9]) if row[9] else []

            scores.append(score)
            reviewers.append(reviewer)

            new_scores = json.dumps(scores)
            new_reviewers = json.dumps(reviewers)

            cursor.execute(
                "UPDATE submissions SET scores=?, reviewers=? WHERE title=?",
                (new_scores, new_reviewers, title)
            )

            conn.commit()

        except Exception as e:
            print("DB Error:", e)

        finally:
            if conn:
                conn.close()