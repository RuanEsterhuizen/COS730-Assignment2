from Validator import Validator
from Database import Database

class SubmissionManager:
    def saveSubmission(self, data:str) -> tuple[dict,int]:
        print("SM: Saving Submission")
        # validate format
        v = Validator()
        valid, msg, data_json = v.validateFormat(data)
        
        if not valid:
            raise Exception(f"Invalid format ({msg})")
        
        # save submission to database
        db = Database()
        confirmation, id = db.saveSubmission(data_json)
        
        if not confirmation:
            raise Exception("SM: Submit artefact to database failed")
        
        return data_json, id
