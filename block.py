import time
import hashlib
import random

class Block(object):

    def __init__(self, num_bloc, previous_hash, transactions, id_contributeur):
        self.num_bloc = num_bloc
        self.id_contributeur = id_contributeur
        self.nonce = 1
        self.preuve = ""
        self.previous_hash = previous_hash
        self.transactions = transactions

    @property
    def get_proof_of_work(self):
        block_string = "{}{}{}{}{}".format(self.num_bloc, self.id_contributeur, self.nonce, self.previous_hash, self.transactions)
        block_hash = hashlib.sha256(block_string.encode()).hexdigest()
        while block_hash[0] != "0" :
            self.nonce = random.randrange(0, 1000)
            block_string = "{}{}{}{}{}".format(self.num_bloc, self.id_contributeur, self.nonce, self.previous_hash, self.transactions)
            block_hash = hashlib.sha256(block_string.encode()).hexdigest()
        return block_hash

    @property
    def get_block_hash(self):
        block_string = "{}{}{}{}{}{}".format(self.num_bloc, self.id_contributeur, self.nonce, self.preuve, self.previous_hash, self.transactions)
        return hashlib.sha256(block_string.encode()).hexdigest()