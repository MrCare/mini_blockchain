#!/bin/bash

# 启动3个区块链节点
python3 src/node.py 5000 &
python3 src/node.py 5001 &
python3 src/node.py 5002 &

wait 