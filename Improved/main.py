# UI.submitResearchOutput(data)

from UI import UI
from SubmissionController import SubmissionController

from EvaluationManager import EvaluationManager
from ReviewerManager import ReviewerManager
from NotificationService import NotificationService
from SubmissionManager import SubmissionManager
from Validator import Validator

def main():
    print("Welcome to the Intelligent Submission and Review System")

    # dependency injection
    em = EvaluationManager()
    rm = ReviewerManager()
    ns = NotificationService()
    sm = SubmissionController()
    v = Validator()

    sc = SubmissionController(em, rm, ns, sm, v)

    # Creating the UI
    ui = UI(sc)
    ui.run()

if __name__ == "__main__":
    main()