class Candidate:

    def __init__(self, _id):
        self.id = _id
        self.__vote_number = 0

    def add_vote(self):
        self.__vote_number += 1

    def __str__(self):
        return f'id: {self.id}: {self.__vote_number}'