class MessageCryptographer:
    @staticmethod
    def encode_message(m, public_key):
        return pow(m, *public_key)

    @staticmethod
    def decode_message(c, private_key):
        return  pow(c, *private_key)
