from Reviewer import Reviewer


class ReviewerManager:
    def __init__(self, evaluationManager, group:str):
        self.em = evaluationManager
        self.group = group

    def filterConflicts(self, reviewerList: list[Reviewer]) -> list[Reviewer]:
        print("RM: Reviewing conflicts")
        # Reviewers can only review outputs from their relevant research groups

        filteredList = [
            reviewer
            for reviewer in reviewerList
            if reviewer.group == self.group
        ]
        return filteredList

    def checkWorkload(self, reviewerList: list[Reviewer]) -> list[Reviewer]:
        print("RM: Checking Workload")
        # reduced for simplicity, remove one reviewer if there is more than one in the list
        return reviewerList[1:] if len(reviewerList) > 1 else reviewerList

    def getAvailableReviewers(self) -> list[Reviewer]:
        print("RM: Getting available reviewers")

        from Database import Database

        db = Database(self.em)
        reviewerList = db.fetchReviewers()
        noConflicts = self.filterConflicts(reviewerList)
        filteredReviewers = self.checkWorkload(noConflicts)
        return filteredReviewers
