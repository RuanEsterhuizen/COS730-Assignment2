import time

class NotificationService:
    def __init__(self, title:str, outcome:str):
        self.title = title
        self.outcome = outcome
    
    def sendNotification(self):
        time.sleep(0.01)
        print(f"NS: Notifying {self.outcome} ({self.title})")