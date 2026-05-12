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
        print("EM: Calculating average")
        return sum(self.scores) / len(self.scores)
    
    def checkConsensus(self) -> bool:
        print("EM: Checking consensus")
        if max(self.scores) - min(self.scores) <= 5:
            return True
        return False
    
    def applyRules(self) -> str:
        print("EM: Applying Rules")
        if not self.checkConsensus():
            return "Revision"
        elif self.calculateAverage() >= 7.5:
            return "Accepted"
        else:
            return "Rejected"
    
    def startEvaluation(self):
        print("EM: Starting Evaluation")
        print(self.scores)
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

