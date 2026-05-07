import random

class Reviewer:
    def __init__(self, name: str, group: str):
        self.name = name
        self.group = group

    def assignReview(self, title:str) -> None:
        print(f"Reviewer: Assigning Review ({self.name} - {title}))")
        from EvaluationManager import EvaluationManager

        # randomly score the work
        score = random.randint(0,10)
        em = EvaluationManager(title)
        em.submitScore(score, self.name)