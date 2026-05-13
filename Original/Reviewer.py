import random

class Reviewer:
    def __init__(self, name: str, group: str, evaluationManager):
        self.name = name
        self.group = group
        self.em = evaluationManager

    def assignReview(self, title:str) -> None:
        print(f"R: Assigning Review ({self.name} - {title})")

    def getScore(self) -> int:
        return random.randint(0,10)