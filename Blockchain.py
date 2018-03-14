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
		pass

	@property
	def last_block(self):
	    # Returns the last Block in the chain
	    pass
	
