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

        data_json, submissionId = sm.saveSubmission(data) # throws exceptions for invalid format and db fail
        rm.assignReviewers(data_json["group"], submissionId) # throws exception if there are no reviewers
        outcome = em.startEvaluation(submissionId)
        ns.sendNotification(data_json["title"], outcome)