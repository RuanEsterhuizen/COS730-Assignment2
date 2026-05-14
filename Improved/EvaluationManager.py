from Database import Database

class EvaluationManager:
    def fetchScores(self, submissionId) -> list[int]:
        db = Database()
        scores = db.fetchScores(submissionId)
        if not scores:
            raise Exception("There are no scores for this submission")
        return scores
    
    def checkConsensus(self, scores: list[int]) -> bool:
        if max(scores) - min(scores) <= 5:
            return True
        return False
    
    def checkAcceptance(self, scores: list[int]) -> bool:
        average = sum(scores) / len(scores)
        if average >= 7.5:
            return True
        return False
    
    def determineOutcome(self, scores: list[int]) -> bool:
        print("EM: Determining Outcome")
        if not self.checkConsensus(scores):
            return "Revision"
        if self.checkAcceptance(scores):
            return "Accepted"
        return "Rejected"

    def startEvaluation(self, submissionId:int) -> str:
        print("EM: Starting Evaluation")
        scores = self.fetchScores(submissionId)
        outcome = self.determineOutcome(scores)
        print(f"Scores: {scores}")
        return outcome
