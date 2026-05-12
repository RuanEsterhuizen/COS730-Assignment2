import time

class NotificationService:
    def __init__(self, title:str):
        self.title = title
    
    def notifyAcceptance(self):
        time.sleep(0.01)
        print(f"NS: Notifying Acceptance ({self.title})")

    def notifyRejection(self):
        time.sleep(0.01)
        print(f"NS: Notifying Rejection ({self.title})")

    def notifyRevision(self):
        time.sleep(0.01)
        print(f"Notifying Revision ({self.title})")