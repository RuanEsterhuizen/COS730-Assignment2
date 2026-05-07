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
        database = Database()
        database.saveScore(self.title, score, reviewer)

    def calculateAverage(self) -> float:
        print("EM: Calculating average")
        return sum(self.scores) / len(self.scores)
    
    def checkConsensus(self) -> bool:
        print("EM: Checking consensus")
        avg = self.calculateAverage()
        if avg > 7.5:
            return True
        return False
    
    def applyRules(self) -> str:
        print("EM: Applying Rules")
        if len(self.scores) == 0:
            return "Revision"
        elif self.checkConsensus():
            return "Accepted"
        else:
            return "Rejected"
    
    def startEvaluation(self):
        outcome = self.applyRules()

        print(self.scores)

        match outcome:
            case "Accepted":
                ns = NotificationService(self.title)
                ns.notifyAcceptance()
            case "Rejected":
                ns = NotificationService(self.title)
                ns.notifyAcceptance()
            case "Revision":
                ns = NotificationService(self.title)
                ns.notifyRevision()
