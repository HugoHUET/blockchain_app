import time
import hashlib

class Block(object):

    def __init__(self, num_bloc, preuve, previous_hash, transactions):
        self.num_bloc = num_bloc
        self.preuve = preuve
        self.previous_hash = previous_hash
        self.transactions = transactions

    @property
    def get_block_hash(self):
        print(self)
        block_string = "{}{}{}{}".format(self.num_bloc, self.preuve, self.previous_hash, self.transactions)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self):
        return "{} - {} - {} - {}".format(self.num_bloc, self.preuve, self.previous_hash, self.transactions)