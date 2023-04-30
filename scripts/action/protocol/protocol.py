import argparse
import os
import yaml

# Default values
config_file = "config.yaml"
hard_gas_limit_per_operation = None
hard_gas_limit_per_block = None
hard_storage_limit_per_operation = None
endorsing_reward_per_slot = None
minimal_block_delay = None
double_baking_punishment = None
consensus_threshold = None

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--config_file", help="Config file path")
parser.add_argument("-o", "--hard_gas_limit_per_operation", help="Hard gas limit per operation")
parser.add_argument("-b", "--hard_gas_limit_per_block", help="Hard gas limit per block")
parser.add_argument("-s", "--hard_storage_limit_per_operation", help="Hard storage limit per operation")
parser.add_argument("-e", "--endorsing_reward_per_slot", help="Endorsing reward per slot")
parser.add_argument("-d", "--minimal_block_delay", help="Minimal block delay")
parser.add_argument("-p", "--double_baking_punishment", help="Double baking punishment")
parser.add_argument("-t", "--consensus_threshold", help="Consensus threshold")
args = parser.parse_args()

# Update values from command line arguments
if args.config_file:
    config_file = args.config_file
if args.hard_gas_limit_per_operation:
    hard_gas_limit_per_operation = args.hard_gas_limit_per_operation
if args.hard_gas_limit_per_block:
    hard_gas_limit_per_block = args.hard_gas_limit_per_block
if args.hard_storage_limit_per_operation:
    hard_storage_limit_per_operation = args.hard_storage_limit_per_operation
if args.endorsing_reward_per_slot:
    endorsing_reward_per_slot = args.endorsing_reward_per_slot
if args.minimal_block_delay:
    minimal_block_delay = args.minimal_block_delay
if args.double_baking_punishment:
    double_baking_punishment = args.double_baking_punishment
if args.consensus_threshold:
    consensus_threshold = args.consensus_threshold

# Check if config file exists
if not os.path.isfile(config_file):
    print(f"Config file not found: {config_file}")
    exit(1)

# Update the values in the config file
with open(config_file, "r") as f:
    config = yaml.safe_load(f)
config["activation"]["protocol_parameters"]["hard_gas_limit_per_operation"] = hard_gas_limit_per_operation
config["activation"]["protocol_parameters"]["hard_gas_limit_per_block"] = hard_gas_limit_per_block
config["activation"]["protocol_parameters"]["hard_storage_limit_per_operation"] = hard_storage_limit_per_operation
config["activation"]["protocol_parameters"]["endorsing_reward_per_slot"] = endorsing_reward_per_slot
config["activation"]["protocol_parameters"]["minimal_block_delay"] = minimal_block_delay
config["activation"]["protocol_parameters"]["double_baking_punishment"] = double_baking_punishment
config["activation"]["protocol_parameters"]["consensus_threshold"] = consensus_threshold
with open(config_file, "w") as f:
    yaml.dump(config, f)

print(f"Values updated in config file: {config_file}")
