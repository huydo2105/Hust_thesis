#!/bin/bash

# Default values
config_file=""
hard_gas_limit_per_operation=""
hard_gas_limit_per_block=""
hard_storage_limit_per_operation=""
endorsing_reward_per_slot=""
minimal_block_delay=""
double_baking_punishment=""
consensus_threshold=""
requirement=""

# Parse command line arguments
while getopts "f:o:b:s:e:d:p:t:r:" opt
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
    r) requirement=$OPTARG;;
  esac
done

# Check if config file is provided
if [ -z "$config_file" ]; then
  echo "Config file not specified."
  exit 1
fi

# Check if config file exists
if [ ! -f "$config_file" ]; then
  echo "Config file not found: $config_file"
  exit 1
fi

# Update the values in the config file
if [ -n "$hard_gas_limit_per_operation" ]; then
  yq w -i "$config_file" activation.protocol_parameters.hard_gas_limit_per_operation "$hard_gas_limit_per_operation"
fi

if [ -n "$hard_gas_limit_per_block" ]; then
  yq w -i "$config_file" activation.protocol_parameters.hard_gas_limit_per_block "$hard_gas_limit_per_block"
fi

if [ -n "$hard_storage_limit_per_operation" ]; then
  yq w -i "$config_file" activation.protocol_parameters.hard_storage_limit_per_operation "$hard_storage_limit_per_operation"
fi

if [ -n "$endorsing_reward_per_slot" ]; then
  yq w -i "$config_file" activation.protocol_parameters.endorsing_reward_per_slot "$endorsing_reward_per_slot"
fi

if [ -n "$minimal_block_delay" ]; then
  yq w -i "$config_file" activation.protocol_parameters.minimal_block_delay "$minimal_block_delay"
fi

if [ -n "$double_baking_punishment" ]; then
  yq w -i "$config_file" activation.protocol_parameters.double_baking_punishment "$double_baking_punishment"
fi

if [ -n "$consensus_threshold" ]; then
  yq w -i "$config_file" activation.protocol_parameters.consensus_threshold "$consensus_threshold"
fi

if [ -n "$requirement" ]; then
  if [ "$requirement" == "safety" ]; then
    # Replace the protocol with Ps9mPmXaRzmzk35gbAYNCAw6UXdE2qoABTHbN2oEEc1qM7CwT9P
    yq w -i "$config_file" activation.protocol Ps9mPmXaRzmzk35gbAYNCAw6UXdE2qoABTHbN2oEEc1qM7CwT9P
  elif [ "$requirement" == "liveness" ]; then
    # Replace the protocol with PtHangzHogokSuiMHemCuowEavgYTP8J5qQ9fQS793MHYFpCY3r
    yq w -i "$config_file" activation.protocol PtHangzHogokSuiMHemCuowEavgYTP8J5qQ9fQS793MHYFpCY3r
  fi
fi


echo "Values updated in config file: $config_file"
