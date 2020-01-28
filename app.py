# coding=UTF-8
print('Hello World!')
from uuid import uuid4

import requests
from flask import Flask, jsonify, url_for, request

from blockchain import BlockChain


app = Flask(__name__)

blockchain = BlockChain()

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

    response = {
        'message': 'Transaction envoyé',
        'transaction': transaction_created,
        'block_created': block
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


if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', default=5000, type=int)
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=True)