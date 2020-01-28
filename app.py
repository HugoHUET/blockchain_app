# coding=UTF-8
import json
import hashlib
import requests
from flask import Flask, jsonify, url_for, request

from blockchain import BlockChain
from block import Block


app = Flask(__name__)

blockchain = BlockChain()

blockchain.nodes.add("http://127.0.0.1:5001")
blockchain.nodes.add("http://127.0.0.1:5002")

@app.route('/create-transaction', methods=['POST'])
def create_transaction():
    """
    [
        {
            "numero_page": "1"
            "texte": "il etait une fois...",
        },
        {
            "numero_page": "1"
            "texte": "il etait une fois...",
        }...
    ]
    """
    transaction_data = request.get_json()

    transaction_created = blockchain.creer_transaction(transaction_data)
    block = blockchain.mine_block()
    is_valid = 0
    for node_address in blockchain.nodes:
        resp = requests.post(node_address + url_for('check_block'), json = block).json()
        if resp["block_valid"] == True:
            is_valid = is_valid+1

    msg = "Transaction envoyé et refusé, block supprimé"
    if is_valid >= 2:
        block = Block(
            num_bloc = block["num_bloc"],
            id_contributeur = block["id_contributeur"],
            nonce = block["nonce"],
            preuve = block["preuve"],
            hash = block["hash"],
            previous_hash = block["previous_hash"],
            transactions = block["transactions"],
        )
        blockchain.chain.append(block)
        msg = 'Transaction envoyé et accepté, block ajouté à la chaine !',
    elif is_valid < 2:
        msg = 'Transaction envoyé mais pas assez de noeuds l\'ont accepté, block supprimé'
    
    print(msg)

    response = {
        'message': msg,
    }

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def get_full_chain():
    response = {
        'chain': blockchain.get_serialized_chain
    }
    return jsonify(response)


@app.route('/register-node', methods=['POST'])
def register_node():

    node_data = request.get_json()

    blockchain.create_node(node_data.get('address'))

    response = {
        'message': 'Le noeud a été ajouté',
        'node_count': len(blockchain.nodes),
        'nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/sync-chain', methods=['GET'])
def consensus():

    def get_neighbour_chains():
        neighbour_chains = []
        for node_address in blockchain.nodes:
            resp = requests.get(node_address + url_for('get_full_chain')).json()
            chain = resp['chain']
            neighbour_chains.append(chain)
        return neighbour_chains

    neighbour_chains = get_neighbour_chains()
    if not neighbour_chains: # Si aucune chaine n'est trouvées
        return jsonify({'message': 'Aucune chaine disponible'})

    longest_chain = max(neighbour_chains, key=len)  # Récup la chaine la plus longue

    if len(blockchain.chain) >= len(longest_chain):  # Si notre chaine est plus grande alors on ne fait rien
        response = {
            'message': 'Le chaine est à jour',
            'chain': blockchain.get_serialized_chain
        }
    else:  # Si notre chaine n'est pas la plus grande alors on la remplace par la plus grande
        blockchain.chain = [blockchain.get_block_object_from_block_data(block) for block in longest_chain]
        response = {
            'message': 'La chaine a été remplacé',
            'chain': blockchain.get_serialized_chain
        }

    return jsonify(response)

@app.route('/check-block', methods=['POST'])
def check_block():

    block_valid = True

    node_block = request.get_json()

    if node_block["num_bloc"] != len(blockchain.chain):
        block_valid = False

    block_string = "{}{}{}{}{}{}".format(node_block["num_bloc"], node_block["id_contributeur"], node_block["nonce"], node_block["preuve"], node_block["previous_hash"], json.dumps(node_block["transactions"]))
    block_hash = hashlib.sha256(block_string.encode()).hexdigest()

    if node_block["hash"] != block_hash:
        block_valid = False

    if block_valid == True:
        block = Block(
            num_bloc = node_block["num_bloc"],
            id_contributeur = node_block["id_contributeur"],
            nonce = node_block["nonce"],
            preuve = node_block["preuve"],
            hash = node_block["hash"],
            previous_hash = node_block["previous_hash"],
            transactions = node_block["transactions"]
        )
        blockchain.chain.append(block)

    response = {
        'block_valid': block_valid,
    }

    return jsonify(response), 201


if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', default=5000, type=int)
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=True)