# coding=UTF-8
import hashlib
import random
import string
import time
import json

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
        self.chain.append(self.create_new_block(previous_hash=""))

    def create_new_block(self, previous_hash):
        block = Block(
            num_bloc = len(self.chain),
            id_contributeur = contributeur_id,
            nonce = 1,
            preuve = "",
            hash = "",
            previous_hash = previous_hash,
            transactions = self.transactions_arr
        )
        block.preuve = block.get_proof_of_work
        block.hash = block.get_block_hash
        self.transactions_arr = []  # Reinitialise la liste de transaction

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

    @property
    def get_last_block(self):
        return self.chain[-1]

    def is_valid_chain(self):
        """
        Check if given blockchain is valid
        """
        previous_block = self.chain[0]
        current_num_bloc = 1

        while current_num_bloc < len(self.chain):

            block = self.chain[current_num_bloc]

            if not self.is_valid_block(block, previous_block):
                return False

            previous_block = block
            current_num_bloc += 1

        return True

    def mine_block(self):

        last_block = self.get_last_block

        last_hash = last_block.get_block_hash
        block = self.create_new_block(last_hash)

        return vars(block)  # Retourne le block créé

    def create_node(self, address):
        self.nodes.add(address)
        return True

    @staticmethod
    def get_block_object_from_block_data(block_data):
        return Block(
            block_data['num_bloc'],
            block_data['id_contributeur'],
            block_data['nonce'],
            block_data['preuve'],
            block_data['previous_hash'],
            block_data['transactions']
        )