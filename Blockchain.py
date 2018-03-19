import hashlib
import json
from time import time
from textwrap import dedent
from uuid import uuid4

from flask import Flask, jsonify, request

class Blockchain(object):
	def __inti__(self):
		self.chain = []
		self.current_transactions = []

		# Create the gensis block
		self.new_block(previous_hash=1, proof=100)

	def new_block(self, proof, previous_hash=None):
		# Creates a new Block and adds it to the chain
		"""
		Creates a new block in the Blockchain

		:param proof: 			<int> The proof given by the Proof of Work algorithm
		:param previous_hash: 	(Optional) <str> Hash of previous block
		:return: 				<dict> New Block 

		"""

		block = {
			'index': len(self.chain) + 1,
			'timestamp': time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash
		}

		# Reset the current list of transactions
		self.current_transactions = []

		self.chain.append(block)
		return block

	def new_transaction(self, sender, recipient, amount):
		# Adds a new transaction to the list of transaction
		"""
		Creates a new transaction to go into the next mined Block

		:param sender: 		<str> Address o f the sender
		:param recipient: 	<str> Address of the recipient
		:param amount: 		<int> Amount
		:return: 			<int> The index of the Block that will hold this transaction
		"""

		self.current_transactions.append({
			'sender': sender,
			'recipient': recipient,
			'amount': amount
		})

		return self.last_block['index']+1

	@staticmethod
	def hash(block):
		# Hashes a block
		"""
		Creates a SHA-256 hash of a Block

		:param block: 	<dict> Block
		:return: 		<str>
		"""
		block_string = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()

	@property
	def last_block(self):
	    # Returns the last Block in the chain
	    return self.chain[-1]
	
	def proof_of_work(self, last_proof):
		"""
		Simple Proof of Work algorithm:
		- Find a number 'p' such that hash(pp') contains 4 leading zeroes, where p is the previous proof, 
		- p' is the new proof

		:param last_proof: 	<int>
		:return:			<int>
		"""

		proof = 0
		while self.valid_proof(last_proof, proof) is False:
			proof += 1

		return proof

	@staticmethod
	def valid_proof(last_proof, proof):
		"""
		Validates the proof:
		Does hash(proof, last_proof) contains 4 leading zeroes?

		:param last_proof:	<int> Previous proof
		:param proof:		<int> Current Proof
		:return:			<bool> True if correct, False if not
		"""

		guess = f'{last_proof}{proof}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()



@app.route('/mine', methods=['GET'])
def mine():
	return "We'll mine a new Block"

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
	values = request.get_json()

	# Check that the required fields are in the POST'ed data
	required = ['sender', 'recipient', 'amount']
	if not all(k in values for k in required):
		return "Missing values", 400

	# Create a new Transaction
	index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
	
	response = {'message': f'Transaction will be added to Block {index}'}
	return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
	response = {
		'chain': blockchain.chain,
		'length': len(blockchain.chain),
	}	
	return jsonify(response), 200


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
