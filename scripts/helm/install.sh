#!/bin/bash

# check for chain name argument
if [ -z "$1" ]; then
    echo "Usage: $0 <chain_name>"
    exit 1
fi

# set chain name
CHAIN_NAME=$1

# Set default values if they were not set by the command line arguments
: ${CHAIN_NAME:=default-chain}

# create Helm release
helm install $CHAIN_NAME oxheadalpha/tezos-chain \
--values ./${CHAIN_NAME}_values.yaml \
--namespace ${CHAIN_NAME} --create-namespace