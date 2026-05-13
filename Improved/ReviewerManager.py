from Reviewer import Reviewer
from Database import Database

class ReviewerManager:
    def filterConflicts(self, reviewerList: list[Reviewer], submissionGroup) -> list[Reviewer]:
        print("RM: Reviewing conflicts")
        # Reviewers can only review outputs from their relevant research groups

        filteredList = [
            reviewer
            for reviewer in reviewerList
            if reviewer.group == submissionGroup
        ]
        return filteredList

    def checkWorkload(self, reviewerList: list[Reviewer]) -> list[Reviewer]:
        print("RM: Checking Workload")
        # reduced for simplicity, remove one reviewer if there is more than one in the list
        return reviewerList[1:] if len(reviewerList) > 1 else reviewerList
    
    def fetchReviewers(self) -> list[Reviewer]:
        # fetch reviewers from the database
        db = Database()
        reviewerListRaw = db.fetchReviewers()

        reviewerList = []
        for r in reviewerListRaw:
            reviewer = Reviewer(r["name"], r["research_group"])
            reviewerList.append(reviewer)

        return reviewerList

    def assignReviewers(self, submissionGroup, submissionId) -> None:
        print("RM: Assigning Reviewers")

        reviewerList = self.fetchReviewers()

        # filter the reviewers
        filteredList = self.filterConflicts(reviewerList, submissionGroup)
        filteredList = self.checkWorkload(filteredList)

        # check if reviewers are available, else return error
        if not filteredList:
            raise Exception("There are no reviewers available at this time")

        # assign reviewers
        scores = []
        for r in filteredList:
            score = r.assignReview()
            scores.append(score)

        # save all scores to the database
        db = Database()
        db.saveScores(submissionId, scores)
