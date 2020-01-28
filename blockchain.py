# coding=UTF-8
import hashlib
import random
import string
import time

from block import Block

contributeur_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(40)])

class BlockChain(object):

    def __init__(self):
        self.chain = []
        self.transactions_arr = []
        self.nodes = set()
        self.create_genesis_block()

    @property
    def get_serialized_chain(self):
        return [vars(block) for block in self.chain]

    def create_genesis_block(self):
        self.create_new_block(previous_hash="")

    def create_new_block(self, previous_hash):
        block = Block(
            num_bloc=len(self.chain),
            id_contributeur=contributeur_id,
            nonce=1,
            preuve="",
            previous_hash=previous_hash,
            transactions=self.transactions_arr
        )
        block.preuve = block.get_proof_of_work
        self.transactions_arr = []  # Reinitialise la liste de transaction

        self.chain.append(block) # Ajoute le bloc dans la chaine
        return block

    @staticmethod
    def is_valid_block(block, previous_block):
        if previous_block.num_bloc + 1 != block.num_bloc:
            return False

        elif previous_block.get_block_hash != block.previous_hash:
            return False

        elif not BlockChain.is_valid_preuve(block.preuve, previous_block.preuve):
            return False

        return True

    def creer_transaction(self, pages):
        pages_arr = []
        for page in pages:
            pages_arr.append({
                'numero_page': page["numero_page"],
                'texte': page["texte"],
                'texte_encrypt': hashlib.sha256(page["texte"].encode('UTF-8')).hexdigest()
            })

        self.transactions_arr = pages_arr

        return True