from backend.wallet.transaction import Transaction
from _pytest.python_api import RaisesContext
from backend.blockchain.block import Block
from backend.wallet.wallet import Wallet 
from backend.config import MINING_REWARD_INPUT

class Blockchain:
    """
    Blockchain a public ledger of transactions.
    Implements as a list of blocks - data sets of transactions 
    """

    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        last_block = self.chain[-1]
        self.chain.append(Block.mine_block(last_block, data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def replace_chain(self, chain):
        '''
        Replace the local chain with the incoming one if:
        - Incoming chain must be longer than the local one
        - The incoming chian is formatted correctly
        '''

        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. The incoming chain must be longer')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')

        self.chain = chain

    def to_json(self):
        '''
        Serialize the blockchain into a list of block
        '''

        # serialized_chain = []

        # for block in self.chain:
        #     serialized_chain.append(block.to_json())

        # return serialized_chain

        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        '''
        Deserialize list of blocks into blockchain instance
        The result will be a chain list of BLock instances
        '''

        blockchian = Blockchain()
        blockchian.chain = list(map(lambda block_json: Block.from_json(block_json), chain_json))

        return blockchian

    @staticmethod
    def is_valid_chain(chain):
        '''
        Validate the incoming chain 
        Enforce the followin rule of the blockchain:
        - Must start with genesis block
        - Blocks must be formatted correctly 
        '''

        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid')


        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)

        Blockchain.is_valid_transaction_chain(chain)

    @staticmethod
    def is_valid_transaction_chain(chain):
        '''
        Enforce the rules of a chain composed of blocks of the transactions.
        - Each transaction must only appear once
        - Only one reward per block
        - Each transaction must be valid  
        '''

        transaction_ids = set()

        for i in range (len(chain)):
            block = chain[i]
            has_mining_reward = False

            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)

                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction: {transaction.id} is not unique')

                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(
                            'There can only be one mining reward per block. '\
                                f'Check block with hash: {block.hash}'
                        )
                    
                    has_mining_reward = True
                
                else:

                    historic_blockchain= Blockchain()

                    historic_blockchain.chain = chain[0:i]

                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input['address']
                    )

                    if historic_balance != transaction.input['amount']:
                        raise Exception(f'Transaction {transaction.id} has an invalid input amount')

                Transaction.is_valid_transaction(transaction)
def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)
    print(f'blockchain.py __name__: {__name__}')

if __name__ == '__main__':
    main()