# 迷你区块链系统

## 项目简介
这是一个基于Python的简化区块链系统，实现了工作量证明（PoW）共识机制、区块链接、网络广播与验证功能。

## 安装依赖
```bash
pip install -r requirements.txt
```

## 演示区块链工作流程

### 场景：多节点交易与区块同步

#### 准备工作
1. 启动多个节点
```bash
# 启动3个节点
python3 src/node.py 5000 &
python3 src/node.py 5001 &
python3 src/node.py 5002 &
```

#### 步骤详解

1. **注册节点**
```bash
# 在节点间建立连接
curl -X POST http://localhost:5000/nodes/register -H "Content-Type: application/json" -d '{"nodes":["http://localhost:5001", "http://localhost:5002"]}'
curl -X POST http://localhost:5001/nodes/register -H "Content-Type: application/json" -d '{"nodes":["http://localhost:5000", "http://localhost:5002"]}'
curl -X POST http://localhost:5002/nodes/register -H "Content-Type: application/json" -d '{"nodes":["http://localhost:5000", "http://localhost:5001"]}'
```

2. **创建交易**
```bash
# 在5000端口节点创建交易
curl -X POST http://localhost:5000/transactions/new -H "Content-Type: application/json" -d '{"sender":"Alice", "recipient":"Bob", "amount":50}'
curl -X POST http://localhost:5000/transactions/new -H "Content-Type: application/json" -d '{"sender":"Charlie", "recipient":"David", "amount":25}'
```

3. **挖掘区块**
```bash
# 在5000端口节点挖掘区块
curl http://localhost:5000/mine
```

4. **验证区块同步**
```bash
# 检查其他节点的区块链状态
curl http://localhost:5001/chain
curl http://localhost:5002/chain
```

<!-- 5. **解决冲突**
```bash
# 如果节点间出现分歧，可以触发共识机制
curl http://localhost:5001/nodes/resolve
curl http://localhost:5002/nodes/resolve # 目前不存在冲突 
```
-->

或使用验证脚本：
```
chmod +x ./show.sh
./show.sh
```

### 预期输出

- 5000端口节点成功打包交易
- 5001和5002节点通过网络同步获得相同的区块链状态
- 交易被成功广播和确认
- 输出日志如下:

```
(base) ➜  mini_blockchain git:(main) ✗ ./show.sh
[2/6] 启动3个区块链节点...
 * Serving Flask app "node" (lazy loading)
 * Serving Flask app "node" (lazy loading)
 * Environment: production
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
   Use a production WSGI server instead.
 * Debug mode: off
 * Debug mode: off
 * Serving Flask app "node" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://localhost:5000/ (Press CTRL+C to quit)
 * Running on http://localhost:5001/ (Press CTRL+C to quit)
 * Running on http://localhost:5002/ (Press CTRL+C to quit)
[3/6] 注册节点间连接...
127.0.0.1 - - [09/Jul/2025 00:30:41] "POST /nodes/register HTTP/1.1" 201 -
127.0.0.1 - - [09/Jul/2025 00:30:41] "POST /nodes/register HTTP/1.1" 201 -
127.0.0.1 - - [09/Jul/2025 00:30:41] "POST /nodes/register HTTP/1.1" 201 -
[4/6] 创建交易...
127.0.0.1 - - [09/Jul/2025 00:30:41] "POST /transactions/new HTTP/1.1" 201 -
[5/6] 挖掘区块...
127.0.0.1 - - [09/Jul/2025 00:30:41] "POST /block/receive HTTP/1.1" 200 -
127.0.0.1 - - [09/Jul/2025 00:30:41] "POST /block/receive HTTP/1.1" 200 -
127.0.0.1 - - [09/Jul/2025 00:30:41] "GET /mine HTTP/1.1" 200 -
{"block":{"index":2,"previous_hash":"ba1f92e95117569d603997dba73c121d628d353dca7f8192560ca73a0d475768","proof":117551,"timestamp":1751992241,"transactions":[{"amount":50,"recipient":"Bob","sender":"Alice","timestamp":1751992241},{"amount":1,"recipient":"ec9faa9f-78bc-4274-846f-e50d87b09f81","sender":"0","timestamp":1751992241}]},"message":"\u65b0\u533a\u5757\u5df2\u6316\u6398"}
[6/6] 验证区块链状态...
节点5000的区块链:
127.0.0.1 - - [09/Jul/2025 00:30:41] "GET /chain HTTP/1.1" 200 -
{
  "chain": [
    {
      "index": 1,
      "previous_hash": "0000000000000000000000000000000000000000000000000000000000000000",
      "proof": 1,
      "timestamp": 1751992238,
      "transactions": []
    },
    {
      "index": 2,
      "previous_hash": "ba1f92e95117569d603997dba73c121d628d353dca7f8192560ca73a0d475768",
      "proof": 117551,
      "timestamp": 1751992241,
      "transactions": [
        {
          "amount": 50,
          "recipient": "Bob",
          "sender": "Alice",
          "timestamp": 1751992241
        },
        {
          "amount": 1,
          "recipient": "ec9faa9f-78bc-4274-846f-e50d87b09f81",
          "sender": "0",
          "timestamp": 1751992241
        }
      ]
    }
  ],
  "length": 2
}
节点5001的区块链:
127.0.0.1 - - [09/Jul/2025 00:30:41] "GET /chain HTTP/1.1" 200 -
{
  "chain": [
    {
      "index": 1,
      "previous_hash": "0000000000000000000000000000000000000000000000000000000000000000",
      "proof": 1,
      "timestamp": 1751992238,
      "transactions": []
    },
    {
      "index": 2,
      "previous_hash": "ba1f92e95117569d603997dba73c121d628d353dca7f8192560ca73a0d475768",
      "proof": 117551,
      "timestamp": 1751992241,
      "transactions": [
        {
          "amount": 50,
          "recipient": "Bob",
          "sender": "Alice",
          "timestamp": 1751992241
        },
        {
          "amount": 1,
          "recipient": "ec9faa9f-78bc-4274-846f-e50d87b09f81",
          "sender": "0",
          "timestamp": 1751992241
        }
      ]
    }
  ],
  "length": 2
}
节点5002的区块链:
127.0.0.1 - - [09/Jul/2025 00:30:41] "GET /chain HTTP/1.1" 200 -
{
  "chain": [
    {
      "index": 1,
      "previous_hash": "0000000000000000000000000000000000000000000000000000000000000000",
      "proof": 1,
      "timestamp": 1751992238,
      "transactions": []
    },
    {
      "index": 2,
      "previous_hash": "ba1f92e95117569d603997dba73c121d628d353dca7f8192560ca73a0d475768",
      "proof": 117551,
      "timestamp": 1751992241,
      "transactions": [
        {
          "amount": 50,
          "recipient": "Bob",
          "sender": "Alice",
          "timestamp": 1751992241
        },
        {
          "amount": 1,
          "recipient": "ec9faa9f-78bc-4274-846f-e50d87b09f81",
          "sender": "0",
          "timestamp": 1751992241
        }
      ]
    }
  ],
  "length": 2
}
已经将新区块打包并广播验证完成出块
```

## 许可证
MIT License 