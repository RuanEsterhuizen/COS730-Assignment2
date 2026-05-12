import random

class Reviewer:
    def __init__(self, name: str, group: str, evaluationManager):
        self.name = name
        self.group = group
        self.em = evaluationManager

    def assignReview(self, title:str) -> None:
        print(f"Reviewer: Assigning Review ({self.name} - {title}))")

        # randomly score the work
        score = random.randint(0,10)
        self.em.submitScore(score, self.name)