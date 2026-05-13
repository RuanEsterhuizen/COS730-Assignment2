from SubmissionManager import SubmissionManager
from ReviewerManager import ReviewerManager
from EvaluationManager import EvaluationManager
from NotificationService import NotificationService

class SubmissionController:
    def submit(self, data):

        print("SC: Submitting research output")
        
        sm = SubmissionManager()
        rm = ReviewerManager()
        em = EvaluationManager()
        ns = NotificationService()

        data_json = sm.saveSubmission(data) # throws exceptions for invalid format and db fail
        scores = rm.assignReviewers(data_json["group"]) # throws exception if there are no reviewers
        outcome = em.EvaluationManager(scores)
        ns.sendNotification(data_json["title"], outcome)