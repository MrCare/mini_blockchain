import uuid
import requests
from flask import Flask, jsonify, request
from blockchain import Blockchain

class BlockchainNode:
    def __init__(self, host='localhost', port=5000):
        self.node_id = str(uuid.uuid4())
        self.blockchain = Blockchain()
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.register_routes()

    def register_routes(self):
        """注册Flask路由"""
        @self.app.route('/mine', methods=['GET'])
        def mine_block():
            """挖掘新区块"""
            block = self.blockchain.mine_block()
            
            # 广播新区块到所有已注册节点
            for node in self.blockchain.nodes:
                try:
                    requests.post(f'{node}/block/receive', json=block)
                except requests.exceptions.RequestException:
                    print(f"无法向节点 {node} 广播区块")
            
            response = {
                'message': '新区块已挖掘',
                'block': block
            }
            return jsonify(response), 200

        @self.app.route('/transactions/new', methods=['POST'])
        def new_transaction():
            """创建新交易"""
            values = request.get_json()
            required = ['sender', 'recipient', 'amount']
            if not all(k in values for k in required):
                return 'Missing values', 400

            transaction = self.blockchain.create_transaction(
                values['sender'], 
                values['recipient'], 
                values['amount']
            )
            response = {'message': f'交易已添加到交易池'}
            return jsonify(response), 201

        @self.app.route('/chain', methods=['GET'])
        def get_full_chain():
            """获取完整区块链"""
            response = {
                'chain': self.blockchain.chain,
                'length': len(self.blockchain.chain)
            }
            return jsonify(response), 200

        @self.app.route('/nodes/register', methods=['POST'])
        def register_nodes():
            """注册新节点"""
            values = request.get_json()
            nodes = values.get('nodes')
            if nodes is None:
                return "Error: 请提供有效的节点列表", 400

            for node in nodes:
                self.blockchain.nodes.add(node)

            response = {
                'message': '新节点已添加',
                'total_nodes': list(self.blockchain.nodes)
            }
            return jsonify(response), 201

        @self.app.route('/nodes/resolve', methods=['GET'])
        def consensus():
            """共识机制：解决节点间的区块链冲突"""
            replaced = self.resolve_conflicts()
            if replaced:
                response = {
                    'message': '本地区块链已被替换',
                    'new_chain': self.blockchain.chain
                }
            else:
                response = {
                    'message': '本地区块链是最新的',
                    'chain': self.blockchain.chain
                }
            return jsonify(response), 200

        @self.app.route('/block/receive', methods=['POST'])
        def receive_new_block():
            """接收并验证新区块"""
            new_block = request.get_json()
            
            # 验证新区块的合法性
            last_block = self.blockchain.chain[-1]
            
            # 验证 previous_hash 是否正确
            if new_block['previous_hash'] != self.blockchain.hash_block(last_block):
                return jsonify({'message': '区块验证失败：前一区块哈希不匹配'}), 400
            
            # 验证工作量证明
            if not self.blockchain.valid_proof(new_block['proof'], new_block['previous_hash']):
                return jsonify({'message': '区块验证失败：工作量证明无效'}), 400
            
            
            # 添加新区块到本地链
            self.blockchain.chain.append(new_block)
            
            return jsonify({
                'message': '新区块已成功接收和验证',
                'block_index': new_block['index']
            }), 200

        @self.app.route('/block/broadcast', methods=['POST'])
        def broadcast_new_block():
            """广播新挖掘的区块到所有已知节点"""
            new_block = request.get_json()
            
            # 遍历所有已注册节点
            for node in self.blockchain.nodes:
                try:
                    # 向每个节点发送新区块
                    response = requests.post(f'{node}/block/receive', json=new_block)
                    if response.status_code != 200:
                        print(f"向节点 {node} 广播区块失败")
                except requests.exceptions.RequestException as e:
                    print(f"广播区块时发生错误：{e}")
            
            return jsonify({'message': '区块广播完成'}), 200


    def resolve_conflicts(self):
        """解决节点间的区块链冲突"""
        neighbours = self.blockchain.nodes
        new_chain = None

        max_length = len(self.blockchain.chain)

        for node in neighbours:
            try:
                response = requests.get(f'{node}/chain')
                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']

                    if length > max_length and self.blockchain.validate_chain(chain):
                        max_length = length
                        new_chain = chain
            except requests.exceptions.RequestException:
                continue

        if new_chain:
            self.blockchain.chain = new_chain
            return True

        return False

    def run(self):
        """启动节点服务器"""
        self.app.run(host=self.host, port=self.port)

def main():
    """主函数，启动区块链节点"""
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    node = BlockchainNode(port=port)
    node.run()

if __name__ == '__main__':
    main() 