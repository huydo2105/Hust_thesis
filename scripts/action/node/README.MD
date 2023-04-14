# Configuring Nodes with YAML

This script allows you to easily add or remove nodes to a YAML configuration file for your blockchain.

## Prerequisites

- [yq](https://mikefarah.gitbook.io/yq/) installed
- Linux via snap: `snap install yq --channel=v3/stable`
- Alternatively, run `sudo wget https://github.com/mikefarah/yq/releases/download/3.4.1/yq_linux_amd64 -O /usr/bin/yq && sudo chmod +x /usr/bin/yq && export PATH=$PATH:/usr/bin/yq`

## Usage

You can run this script with the following command:

./nodes.sh -f my-new-chain_values.yaml -a add -r new_node -m 128Mi -c 500m -n 2


Where `node_name` is the name of the node you want to add, `cpu` is the CPU resource limit for the node, `memory` is the memory resource limit for the node, `num_instances` is the number of instances for the node, and `config.yaml` is the name of the configuration file you want to modify.

To remove a node from the configuration file, you can use the following command:


./nodes.sh -f my-new-chain_values.yaml -a remove -r <node_name>

Where `node_name` is the name of the node you want to remove.