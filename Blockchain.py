class Blockchain(object):
	def __inti__(self):
		self.chain = []
		self.current_transactions = []

	def new_block(self):
		# Creates a new Block and adds it to the chain
		pass

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
	