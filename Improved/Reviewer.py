import random

class Reviewer:
    def __init__(self, name: str, group: str):
        self.name = name
        self.group = group

    def assignReview(self, title:str) -> int:
        print(f"R: Assigning Review ({self.name} - {title})")
        return random.randint(0,10)