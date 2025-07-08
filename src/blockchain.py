import hashlib
import json
import time
import uuid

class Blockchain:
    def __init__(self):
        # 初始化区块链，创建创世区块
        self.chain = []
        self.transaction_pool = []
        self.nodes = set()
        
        # 创建创世区块
        self.create_genesis_block()

    def create_genesis_block(self):
        """创建创世区块"""
        genesis_block = {
            'index': 1,
            'timestamp': int(time.time()),
            'transactions': [],
            'proof': 1,
            'previous_hash': '0' * 64
        }
        self.chain.append(genesis_block)
        return genesis_block

    def hash_block(self, block):
        """计算区块哈希值"""
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """工作量证明：寻找满足难度要求的证明值"""
        last_proof = last_block['proof']
        last_hash = self.hash_block(last_block)

        proof = 0
        while not self.valid_proof(last_proof, proof, last_hash):
            proof += 1

        return proof

    def valid_proof(self, last_proof, proof, last_hash):
        """验证工作量证明是否有效"""
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    def create_transaction(self, sender, recipient, amount):
        """创建新的交易"""
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': int(time.time())
        }
        self.transaction_pool.append(transaction)
        return transaction

    def mine_block(self):
        """挖掘新区块"""
        last_block = self.chain[-1]
        proof = self.proof_of_work(last_block)

        # 为矿工添加奖励交易
        miner_reward = {
            'sender': '0',  # 系统奖励
            'recipient': str(uuid.uuid4()),
            'amount': 1,
            'timestamp': int(time.time())
        }
        self.transaction_pool.append(miner_reward)

        block = {
            'index': len(self.chain) + 1,
            'timestamp': int(time.time()),
            'transactions': self.transaction_pool,
            'proof': proof,
            'previous_hash': self.hash_block(last_block)
        }

        # 清空交易池
        self.transaction_pool = []
        self.chain.append(block)
        return block

    def validate_chain(self, chain):
        """验证整个区块链的有效性"""
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i-1]

            # 验证previous_hash是否正确
            if current_block['previous_hash'] != self.hash_block(previous_block):
                return False

            # 验证工作量证明
            if not self.valid_proof(previous_block['proof'], current_block['proof'], current_block['previous_hash']):
                return False

        return True

    def resolve_conflicts(self, other_chains):
        """解决区块链冲突，采用最长链原则"""
        max_length = len(self.chain)
        longest_chain = self.chain

        for chain in other_chains:
            if len(chain) > max_length and self.validate_chain(chain):
                max_length = len(chain)
                longest_chain = chain

        self.chain = longest_chain
        return self.chain 