import re
import numpy as np
from gym.spaces import Box

DEFAULT_CPU = 250000000.0 #250m
DEFAULT_MEMORY = 6291456.0 #64mi
BLOCK_SIZE_MEAN = 6600000
BLOCK_SIZE_STD = 100000
BALANCE_MAX = 40000
BALANCE_MIN = 0
BLOCK_SIZE_MAX = 11200000
BLOCK_SIZE_MIN = 2000000
REWARD_MAX = 20
REWARD_MIN = 0.5
PUNISHMENT_MAX =  2000
PUNISHMENT_MIN = 5
MAX_MEMORY =  107374182 #1024Mi
MAX_CPU = 1000000000 #1000M
MIN_MEMORY = 3355443 #32Mi
MIN_CPU = 150000000 #150M

def parse_storage_size(size_str):
    size_str = size_str.lower()
    multipliers = {'k': 10**3, 'm': 10**6, 'g': 10**9, 't': 10**12}
    if size_str.endswith('gi'):
        multiplier = 1024 ** 3
        size_str = size_str[:-2]
    elif size_str.endswith('mi'):
        multiplier = 1024 ** 2
        size_str = size_str[:-2]
    else:
        multiplier = multipliers[size_str[-1]]
        size_str = size_str[:-1]

    return float(size_str) * multiplier

def parse_cpu_size(size_str):
    if size_str.endswith('m'):
        return float(size_str[:-1]) * 10**6
    else:
        return float(size_str)

def parse_memory_size(size_str):
    size_str = size_str.lower()
    if size_str.endswith('ki'):
        return float(size_str[:-3]) * 1024
    elif size_str.endswith('mi'):
        return float(size_str[:-3]) * 1024**2
    elif size_str.endswith('gi'):
        return float(size_str[:-3]) * 1024**3
    elif size_str.endswith('ti'):
        return float(size_str[:-3]) * 1024**4
    elif size_str.endswith('kb'):
        return float(size_str[:-2]) * 10**3
    elif size_str.endswith('mb'):
        return float(size_str[:-2]) * 10**6
    elif size_str.endswith('gb'):
        return float(size_str[:-2]) * 10**9
    elif size_str.endswith('tb'):
        return float(size_str[:-2]) * 10**12
    else:
        return float(size_str)

def extract_node(data):
    node_data_start = data.find("Nodes:")
    node_data = data[node_data_start:]
    node_pattern = re.compile(r'([\w-]+):\n\s+Storage size: ([\d\.A-Za-z]+)\n\s+Instances: (\d+)\n(?:\s+Resources:\n\s+requests:\n\s+memory: "([\d\.A-Za-z]+)"\n\s+cpu: "([\d\.A-Za-z]+)"\n\s+limits:\n\s+memory: "([\d\.A-Za-z]+)"\n\s+cpu: "([\d\.A-Za-z]+)"\n)?', re.MULTILINE)
    nodes = {}
    for match in node_pattern.finditer(node_data):
        node_name = match.group(1)
        storage_size_str = match.group(2)
        storage_size = parse_storage_size(storage_size_str)
        instances = int(match.group(3))
        resources = {}
        if match.group(4) is not None:
            memory_str = match.group(4)
            memory = parse_memory_size(memory_str)
            cpu_str = match.group(5)
            cpu = parse_cpu_size(cpu_str)
            limits_memory_str = match.group(6)
            limits_memory = parse_memory_size(limits_memory_str)
            limits_cpu_str = match.group(7)
            limits_cpu = parse_cpu_size(limits_cpu_str)
            requests = {'memory': memory, 'cpu': cpu}
            limit = {'memory': limits_memory, 'cpu': limits_cpu}
            nodes[node_name] = {'storage_size': storage_size, 'instances': instances, 'resources': {'requests': requests, 'limits': limit}}
        else:
            nodes[node_name] = {'storage_size': storage_size, 'instances': instances}
    return nodes

def extract_relevant_variables(data):
    # Extract relevant variables
    gas_op = int(re.findall('Hard gas limit per operation: (\d+)', data)[0])
    gas_block = int(re.findall('Hard gas limit per block: (\d+)', data)[0])
    storage_op = int(re.findall('Hard storage limit per operation: (\d+)', data)[0])
    reward_slot = int(re.findall('Endorsing reward per slot: (\d+)', data)[0])
    delay = int(re.findall('Minimal block delay: (\d+)', data)[0])
    punishment = int(re.findall('Double baking punishment: (\d+)', data)[0])
    threshold = int(re.findall('Consensus threshold: (\d+)', data)[0])
    requirement = re.findall('Requirement: (\w+)', data)[0]
    balances = []
    balance_regex = re.compile(r'([\w-]+):\n\s+key:\s+(\w+)\n\s+is_bootstrap_baker_account:\s+(true|false)\n\s+bootstrap_balance:\s+\'(\d+)\'')
    for match in balance_regex.finditer(data):
        node_name = match.group(1)
        balance = int(match.group(4))
        balances.append(balance)
    return gas_op, gas_block, storage_op, reward_slot, delay, punishment, threshold, requirement, balances

def get_finance(balace, reward, punishment):
    # scale avg_balance_per_node using min-max scaling
    avg_balance_per_node_scaled = (balace - BALANCE_MIN) / (BALANCE_MAX - BALANCE_MIN) * 2 - 1

    reward_scaled = (reward - REWARD_MIN) / (REWARD_MAX - REWARD_MIN) * 2 - 1
    punishment_scaled = (punishment - PUNISHMENT_MIN) / (PUNISHMENT_MAX - PUNISHMENT_MIN) * 2 - 1

    # create finance state vector
    return np.array([avg_balance_per_node_scaled, reward_scaled, punishment_scaled])

def process_state():
    with open('/home/fetia/IdeaProjects/mkchain/scripts/state/result.txt', 'r') as f:
        data = f.read()
    nodes = extract_node(data)
    gas_op, gas_block, storage_op, reward_slot, delay, punishment, threshold, requirement, balances = extract_relevant_variables(data)

    # xtract the relevant information 
    # (storage size, memory, cpu, instances), 
    # calculate the capacity for each node
    memory_capacities = []
    cpu_capacities = []
    total_instances = 0
    for node in nodes.values():
        storage_size = node.get('storage_size', 0)
        request_memory = node.get('resources', {}).get('requests', {}).get('memory', DEFAULT_MEMORY)
        request_cpu = node.get('resources', {}).get('requests', {}).get('cpu', DEFAULT_CPU)
        instances = node.get('instances', 1)
        memory_capacity = request_memory * instances
        cpu_capacity = request_cpu * instances
        memory_capacities.append(memory_capacity)
        cpu_capacities.append(cpu_capacity)
        total_instances += instances 

    # Calculate average balance per node and scale
    avg_balance_per_node = sum(balances) / len(balances)
    
    # Calculate average balance per node and scale
    avg_memory_capacity_per_node = sum(memory_capacities) / total_instances
    avg_cpu_capacity_per_node = sum(cpu_capacities) / total_instances

    # Group variables into features
    block_size = np.array([gas_block])
    memory_capacity = np.array([avg_memory_capacity_per_node])
    cpu_capacity = np.array([avg_cpu_capacity_per_node])
    requirement_feature = np.array([1 if requirement == 'safety' else 0])
    finance = get_finance(avg_balance_per_node, reward_slot, punishment)

    # Scale features
    block_size_scaled = (2 * (block_size - BLOCK_SIZE_MIN) / (BLOCK_SIZE_MAX - BLOCK_SIZE_MIN)) - 1
    memory_capacity_scaled = 2 * (memory_capacity - MIN_MEMORY)/(MAX_MEMORY - MIN_MEMORY) - 1
    cpu_capacity_scaled = 2 * (cpu_capacity - MIN_CPU)/(MAX_CPU - MIN_CPU) - 1

    # Concatenate features into state vector
    state = np.concatenate([block_size_scaled, finance, memory_capacity_scaled, cpu_capacity_scaled, requirement_feature])
    return state
    # # Define the Box space
    # state_space = Box(low=-1, high=1, shape=(5,))
    
    # return state_space.sample()  # Return a random sample from the Box space

print(process_state())
print(process_state().shape)