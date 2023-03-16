#!/bin/bash

BULLET_DIR=$(dirname $0)

while true
do
    read -p "bullet > " INPUT
    python ${BULLET_DIR}/main.py $INPUT
    printf "\n"
done