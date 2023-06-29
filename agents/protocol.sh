#!/bin/bash

# Default values
config_file="my-chain_values.yaml"
hard_gas_limit_per_operation=
hard_gas_limit_per_block=
hard_storage_limit_per_operation=
endorsing_reward_per_slot=
minimal_block_delay=
double_baking_punishment=
consensus_threshold=

# Parse command line arguments
while getopts "f:o:b:s:e:d:p:" opt
do
  case $opt in
    f) config_file=$OPTARG;;
    o) hard_gas_limit_per_operation=$OPTARG;;
    b) hard_gas_limit_per_block=$OPTARG;;
    s) hard_storage_limit_per_operation=$OPTARG;;
    e) endorsing_reward_per_slot=$OPTARG;;
    d) minimal_block_delay=$OPTARG;;
    p) double_baking_punishment=$OPTARG;;
    t) consensus_threshold=$OPTARG;;
  esac
done

# Check if config file exists
if [ ! -f $config_file ]; then
  echo "Config file not found: $config_file"
  exit 1
fi

# Update the values in the config file
yq w -i $config_file activation.protocol_parameters.hard_gas_limit_per_operation $hard_gas_limit_per_operation
yq w -i $config_file activation.protocol_parameters.hard_gas_limit_per_block $hard_gas_limit_per_block
yq w -i $config_file activation.protocol_parameters.hard_storage_limit_per_operation $hard_storage_limit_per_operation
yq w -i $config_file activation.protocol_parameters.endorsing_reward_per_slot $endorsing_reward_per_slot
yq w -i $config_file activation.protocol_parameters.minimal_block_delay $minimal_block_delay
yq w -i $config_file activation.protocol_parameters.double_baking_punishment $double_baking_punishment
yq w -i $config_file activation.protocol_parameters.consensus_threshold $consensus_threshold

echo "Values updated in config file: $config_file"
