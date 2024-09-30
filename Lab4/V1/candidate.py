class Candidate:

    def __init__(self, _id):
        self.__id = _id
        self.__votes_number = 0

    @property
    def id(self):
        return self.__id

    @property
    def votes_number(self):
        return self.__votes_number

    def add_vote(self):
        self.__votes_number += 1

    def __repr__(self):
        return f'Candidate ID: {self.__id}; Votes: {self.votes_number}'