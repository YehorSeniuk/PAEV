class Candidate:

    def __init__(self, _id):
        self.__registration_id = _id
        self.__votes_number = 0

    @property
    def registration_id(self):
        return self.__registration_id

    @registration_id.setter
    def registration_id(self, _id):
        self.__registration_id = _id

    @property
    def votes_number(self):
        return self.__votes_number

    def add_vote(self):
        self.__votes_number += 1

    def __repr__(self):
        return f'Candidate ID: {self.registration_id}; Votes: {self.votes_number}'