#!/bin/bash

conns=$2
rate=$3
ip=$1
echo $conns
echo $rate
httperf --server $ip --port 80 --num-conns $conns --rate $rate --num-calls=1
