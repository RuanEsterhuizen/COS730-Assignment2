import time

class NotificationService:
    def sendNotification(self, title:str, outcome:str):
        time.sleep(0.01)
        print(f"NS: Notifying {outcome} ({title})")