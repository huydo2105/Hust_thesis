from utils.log import log
import os
import subprocess

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
        log("Starting private chain with name " + chain_name + " successfully!", "SUCCESS")
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