from utils.log import log
import subprocess

def deploy_contract(chain):
    # Read the contract code from the file
    contract_file_path = "./contracts/contract.tz"
    try:
        with open(contract_file_path, "r") as contract_file:
            contract_code = contract_file.read()
    except FileNotFoundError:
        log(f"Contract file not found at path '{contract_file_path}'", "ERROR")
        return
    
    # Step 1: Construct the kubectl exec command to write contract_code to contract.tz within the pod
    exec_command = [
        'kubectl',
        '-n', chain,
        'exec', '-i', 'archive-baking-node-0',
        '--', 'sh', '-c',
        'cat > contract.tz'
    ]

    # Start the kubectl exec process
    kubectl_process = subprocess.Popen(
        exec_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Send the contract code to the process' stdin
    kubectl_stdout, kubectl_stderr = kubectl_process.communicate(input=contract_code)

    if kubectl_process.returncode == 0:
        print("Contract code written to contract.tz successfully.")
    else:
        print("Error occurred while writing the contract code.")
        print("Stdout:", kubectl_stdout)
        print("Stderr:", kubectl_stderr)
     
    # Step 2: Deploy the contract using the octez-client command
    octez_command = [
        'kubectl', '-n', chain, 'exec', 'archive-baking-node-0', '--', 'sh', '-c',
        '''octez-client originate contract contract \
        transferring 0 \
        from archive-baking-node-0 running contract.tz \
        --init '(Pair
            "tz1iyd1dExPGVuS7JvueGXF13LZaENVcaPya"
            (Pair
                {
                }
                (Pair
                    {
                    }
                    (Pair
                        {
                            Elt "" 0x68747470733a2f2f6578616d706c652e636f6d
                        }
                        (Pair
                            {
                            }
                            (Pair
                                {
                                }
                                (Pair
                                    {
                                    }
                                    {
                                    })))))))' \
        --fee 0.004671 \
        --gas-limit 10600 \
        --storage-limit 10000'''
    ]
    try:
        result = subprocess.run(octez_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if result.returncode == 0:
            log("Contract deployed successfully.", "SUCCESS")
            # Search for the relevant paragraph in the stdout
            output_lines = result.stdout.splitlines()
            relevant_lines = []
            capture_lines = False

            for line in output_lines:
                if capture_lines:
                    relevant_lines.append(line)
                elif "New contract" in line and "originated." in line or "Contract memorized" in line:
                    capture_lines = True
                    relevant_lines.append(line)

            relevant_paragraph = "\n".join(relevant_lines)

            # Log the relevant paragraph
            log("Contract deployment details:\n" + relevant_paragraph, "INFO")
            
    except subprocess.CalledProcessError as e:
         log(f"Error occurred while deploying contract for chain '{chain}': {e}\nStderr: {e.stderr}", "ERROR")

def update_leader(chain):
    octez_command = [
            'kubectl', '-n', chain, 'exec', 'archive-baking-node-0', '--', 'sh', '-c',
            '''octez-client transfer 0 from archive-baking-node-0 to contract --entrypoint "admin_update_leader" --arg "Pair \"tz1iyd1dExPGVuS7JvueGXF13LZaENVcaPya\" \"Shard-1\"" --burn-cap 1 &
            octez-client transfer 0 from archive-baking-node-0 to contract --entrypoint "admin_update_leader" --arg "Pair \"tz1iyd1dExPGVuS7JvueGXF13LZaENVcaPya\" \"Shard-2\"" --burn-cap 1 &
            octez-client transfer 0 from archive-baking-node-0 to contract --entrypoint "admin_update_leader" --arg "Pair \"tz1iyd1dExPGVuS7JvueGXF13LZaENVcaPya\" \"Shard-3\"" --burn-cap 1'''
        ]
    try:
        result = subprocess.run(octez_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if result.returncode == 0:
            log("Update leader for " + chain + " successfully.", "SUCCESS")

    except subprocess.CalledProcessError as e:
        log(f"Error occurred while updating leader for chain '{chain}': {e}\nStderr: {e.stderr}", "ERROR")

def reveal_node_key(chain):
    octez_command = [
        'kubectl', '-n', chain, 'exec', 'archive-baking-node-0', '--', 'sh', '-c',
        '''octez-client import secret key nodeA unencrypted:edskSAcAFBHJJomYQ6Q8ycyzcVWcpKEwgj5AaLsYwYvaScP2fV543NWMP6kN8bmwiTPhrnBvnmEugQEF5axTTtgxmUCxqJaGLA --force &
        octez-client import secret key nodeB unencrypted:edskRpm2mUhvoUjHjXgMoDRxMKhtKfww1ixmWiHCWhHuMEEbGzdnz8Ks4vgarKDtxok7HmrEo1JzkXkdkvyw7Rtw6BNtSd7MJ7 --force &
         octez-client import secret key nodeC unencrypted:edskS1Vw8yMGpJTEWh4M7Yzu1h8HVPcwPPxZxFLUx41V4Pctyss8zQDgi2LvXtfzJHhFzMwgwJ6VXezidniysoVApJo7vDYN3G --force '''
    ]
    try:
        result = subprocess.run(octez_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if result.returncode == 0:
            log("Reveal node identities successfully.", "SUCCESS")

    except subprocess.CalledProcessError as e:
         log(f"Error occurred while deploying contract for chain '{chain}': {e}\nStderr: {e.stderr}", "ERROR")