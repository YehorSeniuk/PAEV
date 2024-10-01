class Vote:

    def __init__(self, candidate_id, v_token):
        self.__encrypted_candidate_id, self.__encrypted_len, self.__public_bbs_key, self.__encrypted_voter_id = v_token.encrypt(candidate_id)

    @property
    def encoded_candidate_id(self):
        return self.__encrypted_candidate_id

    @property
    def encrypted_len(self):
        return self.__encrypted_len

    @property
    def encrypted_public_key(self):
        return self.__public_bbs_key

    @property
    def encoded_voter_id(self):
        return self.__encrypted_voter_id

