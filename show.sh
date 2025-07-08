#!/bin/bash
###
 # @Author: Mr.Car
 # @Date: 2025-07-09 00:22:52
### 

# 设置颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 执行前检查Python和pip是否已安装
# 清理之前的进程
pkill -f "python3 src/node.py"
sleep 2

# 启动多个节点
echo -e "${YELLOW}[2/6] 启动3个区块链节点...${NC}"
python3 src/node.py 5000 &
python3 src/node.py 5001 &
python3 src/node.py 5002 &
sleep 3

# 注册节点
echo -e "${YELLOW}[3/6] 注册节点间连接...${NC}"
curl -s -X POST http://localhost:5000/nodes/register -H "Content-Type: application/json" -d '{"nodes":["http://localhost:5001", "http://localhost:5002"]}' > /dev/null
curl -s -X POST http://localhost:5001/nodes/register -H "Content-Type: application/json" -d '{"nodes":["http://localhost:5000", "http://localhost:5002"]}' > /dev/null
curl -s -X POST http://localhost:5002/nodes/register -H "Content-Type: application/json" -d '{"nodes":["http://localhost:5000", "http://localhost:5001"]}' > /dev/null

# 创建交易
echo -e "${YELLOW}[4/6] 创建交易...${NC}"
curl -s -X POST http://localhost:5000/transactions/new -H "Content-Type: application/json" -d '{"sender":"Alice", "recipient":"Bob", "amount":50}' > /dev/null

# 挖掘区块
echo -e "${YELLOW}[5/6] 挖掘区块...${NC}"
curl -s http://localhost:5000/mine

# 验证区块链状态
echo -e "${YELLOW}[6/6] 验证区块链状态...${NC}"
echo -e "${GREEN}节点5000的区块链:${NC}"
curl -s http://localhost:5000/chain | jq

echo -e "${GREEN}节点5001的区块链:${NC}"
curl -s http://localhost:5001/chain | jq

echo -e "${GREEN}节点5002的区块链:${NC}"
curl -s http://localhost:5002/chain | jq

# 清理进程
pkill -f "python3 src/node.py"

echo -e "${GREEN}已经将新区块打包并广播验证完成出块${NC}" 