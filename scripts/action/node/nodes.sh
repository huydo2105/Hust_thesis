#!/bin/bash

# Check if config file is provided as an argument
if [ $# -eq 0 ]
  then
    echo "No config file provided. Usage: ./nodes.sh -f <config_file> -a <add|remove> -r <node_name> -m <memory> -c <cpu> [-n <num_instances>]"
    exit 1
fi

# Parse command line arguments
while getopts "f:a:r:m:c:n:" opt
do
  case $opt in
    f) config_file=$OPTARG;;
    a) action=$OPTARG;;
    r) node_name=$OPTARG;;
    m) memory=$OPTARG;;
    c) cpu=$OPTARG;;
    n) num_instances=$OPTARG;;
  esac
done

# Check if the config file exists
if [ ! -f "$config_file" ]
  then
    echo "Config file not found."
    exit 1
fi

# Load the config file
config=$(cat $config_file)

# Define the function to add a new node
function add_node() {
  node_name=$1
  resources=$2
  num_instances=$3

  # Check if the node already exists in the config
  if [[ $(echo "$config" | /usr/bin/yq r - "nodes.$node_name") ]]
    then
      echo "Node $node_name already exists in the config."
      exit 1
  fi

  # Add the new node to the config
  config=$(echo "$config" | /usr/bin/yq w - "nodes.$node_name.storage_size" "15Gi")
  config=$(echo "$config" | /usr/bin/yq w - "nodes.$node_name.resources.requests.memory" "${resources['memory']}")
  config=$(echo "$config" | /usr/bin/yq w - "nodes.$node_name.resources.limits.memory" "${resources['memory']}")
  config=$(echo "$config" | /usr/bin/yq w - "nodes.$node_name.resources.requests.cpu" "${resources['cpu']}")
  config=$(echo "$config" | /usr/bin/yq w - "nodes.$node_name.resources.limits.cpu" "${resources['cpu']}")

  for (( i=0; i<num_instances; i++ )); do
    config=$(echo "$config" | /usr/bin/yq w - "nodes.$node_name.instances.[+]" "{}")
    config=$(echo "$config" | /usr/bin/yq w - "nodes.$node_name.instances.[$i].is_bootstrap_node" "false")
    config=$(echo "$config" | /usr/bin/yq w - "nodes.$node_name.instances.[$i].cofig.shell.history_mode" "rolling")
    config=$(echo "$config" | /usr/bin/yq w - "nodes.$node_name.instances.[$i].cofig.metrics_addr" ":9932")
  done

   # Write the modified config to the config file
  echo "$config" > "$config_file"

  echo "Node $node_name added to the config with $num_instances instances."
}

# Define the function to remove an existing node
function remove_node() {
  node_name=$1

  # Check if the node already exists in the config
  if [[ ! $(echo "$config" | /usr/bin/yq r - "nodes.$node_name") ]]
    then
      echo "Node $node_name already exists in the config."
      exit 1
  fi

  # Remove the node from the config
  config=$(echo "$config" | /usr/bin/yq d - "nodes.$node_name")

  # Write the modified config to the config file
  echo "$config" > "$config_file"

  echo "Remove node '$node_name' from the config file."
}

# Perform the action based on the command line arguments
case $action in
  add)
    declare -A resources=( ["memory"]=$memory ["cpu"]=$cpu )
    add_node "$node_name" resources "$num_instances"
    ;;
  remove)
    remove_node "$node_name"
    ;;
  *)
    echo "Invalid action. Available actions: add, remove."
    exit 1
esac

