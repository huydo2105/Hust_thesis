import os
import subprocess
import sys
import json
import time
import datetime
import yaml
from ddpg import run_algo
from utils.log import log
from utils.dict import convert_dict_to_yaml
from utils.chain import start_private_chain, stop_chain, restart_chain

def monitor_chain_level(chains):
    one_cycle = 16384
    while True:
        for chain, port in chains.items():
            output = subprocess.run(['wget', '-qO-', f'http://localhost:{port}/chains/main/blocks/head/'],
                                    capture_output=True, text=True)
            if output.returncode == 0:
                rpc_result = json.loads(output.stdout)
                current_level = rpc_result["header"]["level"]
                log("Current level of " + chain + " is: " + str(current_level), "INFO")
                if current_level % one_cycle == 0:
                    get_chain_state(chain)
                    run_algo(chain)
            else:
                log(f"Failed to retrieve chain level for '{chain}'. Exiting the loop.", "ERROR")
                time.sleep(15)
                break

            # Add a delay before checking the chain level again
            time.sleep(5)

def get_chain_state(chain_name):
    values_file = f"./{chain_name}_values.yaml"
    write_file = f"./{chain_name}_values.txt"
    log("Reading chain state from " + values_file, "INFOR")
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

def port_forward_chain(chain_name, port):
    command = ['kubectl', 'port-forward', 'archive-baking-node-0', '-n', chain_name, f'{port}:8732']
    try:
        # Check the pod status before proceeding
        pod_status = get_pod_status(chain_name)
        while pod_status != "Running":
            log(f"Pod for chain '{chain_name}' is not running. Waiting for the pod to start.", "INFO")
            time.sleep(10)  # Adjust the delay as needed
            pod_status = get_pod_status(chain_name)

        log(f"Pod for chain '{chain_name}' is running.", "INFO")
        log(f"Initiating port forwarding for chain '{chain_name}' on port {port}.", "INFOR")
        process = subprocess.Popen(command, start_new_session=True)
        if process.poll() is None:
            log(f"Port forwarding initiated for chain '{chain_name}' on port {port}.", "SUCCESS")
            log(f"Port forwarding successful for chain '{chain_name}' on port {port}.", "SUCCESS")
        else:
            log(f"Error occurred while starting port forwarding for chain '{chain_name}' on port {port}", "ERROR")

    except Exception as e:
        log(f"Error occurred while port forwarding for chain '{chain_name}' on port {port}: {e}", "ERROR")

def get_pod_status(chain_name):
    command = ['kubectl', 'get', 'pods', '-n', chain_name, '-o', 'json']
    try:
        output = subprocess.run(command, capture_output=True, text=True, check=True)
        json_output = json.loads(output.stdout)
        pod_status = json_output["items"][1]["status"]["phase"]
        return pod_status
    except Exception as e:
        log(f"Error occurred while getting pod status for chain '{chain_name}': {e}", "ERROR")
        return None


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please provide the number of chains and chain names as command-line arguments.')
        sys.exit(1)

    num_chains = int(sys.argv[1])
    chain_names = sys.argv[2:2+num_chains]

    port = 8733  # Starting port number

    chains = {}  # Dictionary to store chain name and port

    for chain in chain_names:
        log("Starting private chain with name " + chain, "INFO")
        start_private_chain(chain)
        chains[chain] = port  # Store chain name and port in the dictionary
        port += 1  # Increment port number for the next chain

    for chain, port in chains.items():
        log("Port forwarding for chain: " + chain, "INFO")
        port_forward_chain(chain, port)

    while True:
        monitor_chain_level(chains)