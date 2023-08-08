#!/bin/bash

# Parse command line arguments
while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -b|--num-bakers)
        NUM_BAKERS="$2"
        shift
        shift
        ;;
        -n|--num-nodes)
        NUM_NODES="$2"
        shift
        shift
        ;;
        -c|--chain-name)
        CHAIN_NAME="$2"
        shift
        shift
        ;;
        *)
        echo "Unknown option: $1"
        exit 1
        ;;
    esac
done

# Set default values if they were not set by the command line arguments
: ${NUM_BAKERS:=1}
: ${NUM_NODES:=0}
: ${CHAIN_NAME:=my-chain}

mkchain $CHAIN_NAME --number-of-bakers $NUM_BAKERS --number-of-nodes $NUM_NODES


