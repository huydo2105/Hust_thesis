import os
import subprocess
import sys
import json
import time
import datetime
import yaml
from colorama import init, Fore, Style
from ddpg import run_algo
from utils.log import log

# Initialize colorama
init(autoreset=True)

def start_private_chain(chain_name):
    # Set environment variables
    os.environ['CHAIN_NAME'] = chain_name
    os.environ['PYTHONUNBUFFERED'] = 'x'

    # Generate Helm values
    subprocess.run(['mkchain', chain_name])

    # Set Helm release values
    values_file = f'./{chain_name}_values.yaml'
    namespace = chain_name

    # Create Helm release to start the chain
    command = ['helm', 'install', chain_name, 'oxheadalpha/tezos-chain',
           '--values', values_file, '--namespace', namespace, '--create-namespace']

    result = subprocess.run(command)

    if result.returncode == 0:
        log("Starting private chain with name " + chain_name +  " successfully!", "SUCCESS")
    else:
        log(f"Command failed with return code: {result.returncode}", "ERROR")
    
def stop_chain(chain_name):
    command = ['minikube', 'stop']
    try:
        subprocess.run(command, check=True)
        log("Minikube stopped successfully.", "SUCCESS")
    except subprocess.CalledProcessError as e:
        log(f"Error occurred while stopping Minikube: {e}", "ERROR")

def restart_chain(chain_name):
    command = ['minikube', 'start']
    try:
        subprocess.run(command, check=True)
        log("Minikube started successfully.", "SUCCESS")
    except subprocess.CalledProcessError as e:
        log(f"Error occurred while starting Minikube: {e}", "ERROR")

def monitor_chain_level(chain_name):
    # one_cycle = 16384
    one_cycle = 47160
    while True:
        output = subprocess.run(['wget', '-qO-', 'http://localhost:8732/chains/main/blocks/head/'], capture_output=True, text=True)
        if output.returncode == 0:
            rpc_result = json.loads(output.stdout)
            current_level = rpc_result["header"]["level"]
            log("Current level of " + chain_name + " is: " + str(current_level), "INFO")
            if current_level % one_cycle == 0:
                get_chain_state(chain_name)
                run_algo(chain_name)
        else:
            log("Failed to retrieve chain level. Exiting the loop.", "ERROR")
            break

        # Add a delay before checking the chain level again
        time.sleep(5)

def convert_dict_to_yaml(dictionary):
    yaml_output = ""
    for key, value in dictionary.items():
        yaml_output += key + ":\n"
        for inner_key, inner_value in value.items():
            if isinstance(inner_value, bool):
                inner_value = str(inner_value).lower()
            elif isinstance(inner_value, int):
                inner_value = str(inner_value)
            yaml_output += "  " + inner_key + ": " + inner_value + "\n"
    return yaml_output

def get_chain_state(chain_name): 
    values_file = f"./{chain_name}_values.yaml"
    write_file = f"./{chain_name}_values.txt"
    log("Reading chain state from " +values_file, "INFOR")
    # Parse YAML file and extract required fields
    with open(values_file, 'r') as file:
        config = yaml.safe_load(file)

    try:
        requirement = config['requirement']  
    except Exception:
        requirement = None
    hard_gas_limit_per_operation = config['activation']['protocol_parameters']['hard_gas_limit_per_operation']
    hard_gas_limit_per_block = config['activation']['protocol_parameters']['hard_gas_limit_per_block']
    hard_storage_limit_per_operation = config['activation']['protocol_parameters']['hard_storage_limit_per_operation']
    endorsing_reward_per_slot = config['activation']['protocol_parameters']['endorsing_reward_per_slot']
    minimal_block_delay = config['activation']['protocol_parameters']['minimal_block_delay']
    double_baking_punishment = config['activation']['protocol_parameters']['double_baking_punishment']
    consensus_threshold = config['activation']['protocol_parameters']['consensus_threshold']
    balances = config['accounts']
    balances = convert_dict_to_yaml(balances)
    node_info = "Nodes:\n"

    for node in config['nodes']:
        if config['nodes'][node]:
            resources = config['nodes'][node].get('resources')
            storage_size = config['nodes'][node].get('storage_size')
            instances = config['nodes'][node].get('instances')
            if resources or storage_size:
                node_info += f"{node}:\n"
                if storage_size:
                    node_info += f"  Storage size: {storage_size}\n"
                if instances:
                    num_instances = len(instances)
                    node_info += f"  Instances: {num_instances}\n"
                if resources:
                    resources_str = '\n'.join(f"\t\t{resource}" for resource in resources)
                    node_info += f"  Resources:\n{resources_str}\n"

    # Save results in a new file
    log("Writing chain state to " + write_file, "INFOR")
    with open(write_file, 'w') as file:
        file.write(f"Requirement: {requirement}\n\n")
        file.write(f"Hard gas limit per operation: {hard_gas_limit_per_operation}\n")
        file.write(f"Hard gas limit per block: {hard_gas_limit_per_block}\n")
        file.write(f"Hard storage limit per operation: {hard_storage_limit_per_operation}\n")
        file.write(f"Endorsing reward per slot: {endorsing_reward_per_slot}\n")
        file.write(f"Minimal block delay: {minimal_block_delay}\n")
        file.write(f"Double baking punishment: {double_baking_punishment}\n")
        file.write(f"Consensus threshold: {consensus_threshold}\n\n")
        file.write("Balances of each node:\n")
        file.write(f"{balances}\n")
        file.write(node_info)
    log("Writing chain state to " + write_file + " successfully!", "SUCCESS")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide a chain name as a command-line argument.')
        sys.exit(1)

    chain_name = sys.argv[1]
    log("Starting private chain with name " + chain_name, "INFO")
    start_private_chain(chain_name)

    while True:
        monitor_chain_level(chain_name)
