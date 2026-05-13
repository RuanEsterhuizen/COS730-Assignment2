# UI.submitResearchOutput(data)

from UI import UI
from SubmissionController import SubmissionController

def main():
    print("Welcome to the Intelligent Submission and Review System")

    # dependency injection - UI no longer responsible for object creation
    sc = SubmissionController()

    # Creating the UI
    ui = UI(sc)
    ui.run()

if __name__ == "__main__":
    main()