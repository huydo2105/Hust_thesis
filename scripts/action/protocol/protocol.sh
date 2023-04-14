#!/bin/bash

# Parse command line arguments
while getopts "f:a:r:m:c:n:" opt; do
  case $opt in
    f) config_file=$OPTARG;;
    a) action=$OPTARG;;
    r) node_name=$OPTARG;;
    m) memory=$OPTARG;;
    c) cpu=$OPTARG;;
    n) num_instances=$OPTARG;;
  esac
done

# Load the configuration file
eval $(yq -j e $config_file | jq -r '.[] | select(.name=="'"$node_name"'") | "name=\(.name) image=\(.image) memory=\(.memory) cpu=\(.cpu) num_instances=\(.num_instances)"')

# Update configuration values
if [[ ! -z "$memory" ]]; then
  eval memory=$memory
fi
if [[ ! -z "$cpu" ]]; then
  eval cpu=$cpu
fi
if [[ ! -z "$num_instances" ]]; then
  eval num_instances=$num_instances
fi

# Save the updated configuration
yq -i e --arg name "$name" --arg image "$image" --arg memory "$memory" --arg cpu "$cpu" --argjson num_instances "$num_instances" '.[] | select(.name==$name) | .image=$image | .memory=($memory // .memory) | .cpu=($cpu // .cpu) | .num_instances=($num_instances // .num_instances)' $config_file