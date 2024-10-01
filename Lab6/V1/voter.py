import random
from vote import Vote
class Voter:

    def __init__(self):
        self.__login = None
        self.__password = None
        self.__v_token = None

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, login):
        self.__login = login

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def v_token(self):
        return self.__v_token

    @v_token.setter
    def v_token(self, v_token):
        self.__v_token = v_token

    def make_vote(self, candidates):
        candidate = random.choice(candidates)
        candidate_id = candidate.registration_id
        return Vote(candidate_id, self.__v_token)