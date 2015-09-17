#!/bin/bash

conns=$1
rate=$2
echo $conns
echo $rate
httperf --server 10.1.0.39 --port 80 --num-conns $conns --rate $rate
