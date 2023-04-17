#!/bin/bash

# Check if config file path is provided
if [ $# -ne 1 ]; then
  echo "Usage: $0 <config_file_path>"
  exit 1
fi

config_file=$1

# Parse YAML file and extract required fields
requirement=$(yq r "$config_file" requirement)
hard_gas_limit_per_operation=$(yq r "$config_file" activation.protocol_parameters.hard_gas_limit_per_operation)
hard_gas_limit_per_block=$(yq r "$config_file" activation.protocol_parameters.hard_gas_limit_per_block)
hard_storage_limit_per_operation=$(yq r "$config_file" activation.protocol_parameters.hard_storage_limit_per_operation)
endorsing_reward_per_slot=$(yq r "$config_file" activation.protocol_parameters.endorsing_reward_per_slot)
minimal_block_delay=$(yq r "$config_file" activation.protocol_parameters.minimal_block_delay)
double_baking_punishment=$(yq r "$config_file" activation.protocol_parameters.double_baking_punishment)
consensus_threshold=$(yq r "$config_file" activation.protocol_parameters.consensus_threshold)
balances=$(yq r "$config_file" accounts)
node_info="Nodes:\n"

while IFS= read -r node; do
  resources=$(yq r "$config_file" "nodes.$node.resources" 2>/dev/null)
  storage_size=$(yq r "$config_file" "nodes.$node.storage_size" 2>/dev/null)
  instances=$(yq r "$config_file" "nodes.$node.instances" 2>/dev/null)
  if [ -n "$resources" ] || [ -n "$storage_size" ]; then
    node_info+="$node:\n"
    if [ -n "$storage_size" ]; then
      node_info+="  Storage size: $storage_size\n"
    fi
    if [ -n "$instances" ]; then
      num_instances=$(echo "$instances" | yq r - --length)
      node_info+="  Instances: $num_instances\n"
    fi
    if [ -n "$resources" ]; then
      resources=$(echo "$resources" | sed 's/^/\t\t/g')
      node_info+="  Resources:\n$resources\n"
    fi
  fi
done < <(yq r "$config_file" nodes -j | jq -r 'keys[]')

# Save results in new file

cat << EOF > result.txt
Requirement: $requirement

Hard gas limit per operation: $hard_gas_limit_per_operation
Hard gas limit per block: $hard_gas_limit_per_block
Hard storage limit per operation: $hard_storage_limit_per_operation
Endorsing reward per slot: $endorsing_reward_per_slot
Minimal block delay: $minimal_block_delay
Double baking punishment: $double_baking_punishment
Consensus threshold: $consensus_threshold

Balances of each node:
$balances
EOF

echo -e "$node_info" >> result.txt