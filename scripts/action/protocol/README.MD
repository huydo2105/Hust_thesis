# Configuration Updater

This tool is a bash script to update a configuration file in YAML format. It accepts command line arguments to specify which values to update and what the new values should be. The script is designed to handle updates to multiple parameters at once and can take in the YAML configuration file via the command line.

## Dependencies

- yq (v4.x)
- bash (v4.x)

## Usage

Usage: protocol.sh [-h] [-f FILE] [-a ACTION] [-r NODE] [-m MEMORY] [-c CPU] [-n NUM_INSTANCES] [-o HARD_GAS_LIMIT_PER_OPERATION] [-b HARD_GAS_LIMIT_PER_BLOCK] [-s HARD_STORAGE_LIMIT_PER_OPERATION] [-e ENDORSING_REWARD_PER_SLOT] [-d MINIMAL_BLOCK_DELAY] [-p DOUBLE_BAKING_PUNISHMENT] [-t CONSENSUS_THRESHOLD]

Options:
-h Show help message and exit
-f FILE The YAML configuration file to update
-a ACTION The action to perform (update or create)
-r NODE The name of the node to update
-m MEMORY The new memory limit for the node
-c CPU The new CPU limit for the node
-n NUM_INSTANCES The new number of instances for the node
-o VALUE The new hard gas limit per operation
-b VALUE The new hard gas limit per block
-s VALUE The new hard storage limit per operation
-e VALUE The new endorsing reward per slot
-d VALUE The new minimal block delay
-p VALUE The new double baking punishment
-t VALUE The new consensus threshold

## Examples

### Update memory and CPU limits
./protocol.sh -f config.yaml -a update -r node1 -m 4G -c 4

### Update the hard gas limit per block and hard storage limit per operation
./protocol.sh -f config.yaml -a update -r node1 -b 10000000 -s 20000
### Update multiple parameters at once
./protocol.sh -f config.yaml -a update -r node1 -m 4G -c 4 -n 2 -b 10000000 -s 20000 -e 5000 -d 10 -p 100000000 -t 5000
