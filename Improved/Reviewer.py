import random

class Reviewer:
    def __init__(self, name: str, group: str):
        self.name = name
        self.group = group

    def assignReview(self) -> int:
        print(f"R: Assigning Review ({self.name})")
        return random.randint(0,10)