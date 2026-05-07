from Reviewer import Reviewer


class ReviewerManager():
    def filterConflicts(self, reviewerList: list[Reviewer]) -> list[Reviewer]:
        print("RM: Reviewing conflicts")
        filteredList = reviewerList
        
        # TODO: remove all the reviewers where reviewer.busy = true

        return filteredList

    def checkWorkload(self, reviewerList: list[Reviewer]) -> list[Reviewer]:
        print("RM: Checking Workload")
        filteredList = reviewerList

        # TODO: remove all the reviewers that are too busy

        return filteredList

    def getAvailableReviewers(self) -> list[Reviewer]:
        print("RM: Getting available reviewers")

        from Database import Database

        db = Database()
        reviewerList = db.fetchReviewers()
        noConflicts = self.filterConflicts(reviewerList)
        filteredReviewers = self.checkWorkload(noConflicts)
        return filteredReviewers
