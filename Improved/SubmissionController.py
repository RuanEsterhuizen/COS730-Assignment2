import json

class SubmissionController:
    def __init__(self, evaluationManager, reviewerManager, notificationService, submissionManager, validator):
        self.em = evaluationManager
        self.rm = reviewerManager
        self.ns = notificationService
        self.sm = submissionManager
        self.v = validator

    def submit(self, data):

        print("SC: Submitting research output")
        valid, msg = self.v.validateFormat(data)

        if valid[0]:
            data_json = json.loads(data)

            self.sm.saveSubmission(data_json)
            scores = self.rm.assignReviewers(data_json["group"])
            outcome = self.em.EvaluationManager(scores)
            self.ns.sendNotification(data_json["title"], outcome)
            
        else:
            print("SC: Invalid Data Format")
            raise Exception(f"SC: Invalid Data Format ({msg})")