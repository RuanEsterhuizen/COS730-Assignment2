from Database import Database
from NotificationService import NotificationService

class EvaluationManager:
    def __init__(self, title: str):
        self.scores = []
        self.reviewers = []
        self.title = title

    def submitScore(self, score, reviewer):
        print("EM: Submitting score")
        self.scores.append(score)
        self.reviewers.append(reviewer)
        database = Database(self)
        database.saveScore(self.title, score, reviewer)

    def calculateAverage(self) -> float:
        if not self.scores:
            return 0
        return sum(self.scores) / len(self.scores)
    
    def checkConsensus(self) -> bool:
        if not self.scores:
            return False

        if max(self.scores) - min(self.scores) <= 5:
            return True
        return False
    
        
    def applyRules(self) -> str:
        print("EM: Calculating average")
        average = self.calculateAverage()

        print("EM: Checking consensus")
        consensus = self.checkConsensus()

        print("EM: Applying Rules")

        if not consensus:
            return "Revision"
        elif average >= 7.5:
            return "Accepted"
        else:
            return "Rejected"
    
    def startEvaluation(self, reviewers: list):
        print("EM: Starting Evaluation")    

        for reviewer in reviewers:
            score = reviewer.getScore()
            self.submitScore(score, reviewer.name)

        outcome = self.applyRules()

        match outcome:
            case "Accepted":
                ns = NotificationService(self.title)
                ns.notifyAcceptance()
            case "Rejected":
                ns = NotificationService(self.title)
                ns.notifyRejection()
            case "Revision":
                ns = NotificationService(self.title)
                ns.notifyRevision()

