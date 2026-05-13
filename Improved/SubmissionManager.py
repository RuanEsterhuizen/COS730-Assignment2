from Validator import Validator
from Database import Database

class SubmissionManager:
    def saveSubmission(data:str) -> dict:
        # validate format
        v = Validator()
        valid, msg, data_json = v.validateFormat(data)
        
        if not valid:
            raise Exception(f"SM: Invalid format ({msg})")
        
        # save submission to database
        db = Database()
        confirmation = db.saveSubmission(data_json)
        
        if not confirmation:
            raise Exception("SM: Submit artefact to database failed")
