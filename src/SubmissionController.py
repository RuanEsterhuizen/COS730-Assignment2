import json

class SubmissionController():
    def submit(self, data):
        from EvaluationManager import EvaluationManager
        from Validator import Validator
        from Database import Database
        from ReviewerManager import ReviewerManager

        data_json = json.loads(data)

        print("SC: Submitting research output")
        v = Validator()
        valid = v.validateFormat(data_json)

        if valid:
            db = Database()
            confirmation = db.saveSubmission(data_json)

            if not confirmation:
                raise Exception("SC: Save Submission to database failed")

            reviewer_man = ReviewerManager()
            filteredReviewers = reviewer_man.getAvailableReviewers()

            for reviewer in filteredReviewers:
                reviewer.assignReview(data_json["title"])

            eval_man = EvaluationManager(data_json["title"])
            eval_man.startEvaluation()
        else:
            print("SC: Invalid Data Format")
            raise Exception("SC: Invalid Data Format")