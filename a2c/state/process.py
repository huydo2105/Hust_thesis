import re
import numpy as np

import re

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

with open('/home/fetia/IdeaProjects/mkchain/scripts/state/result.txt', 'r') as f:
    data = f.read()

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

print(nodes)


# Extract relevant variables
gas_op = int(re.findall('Hard gas limit per operation: (\d+)', data)[0])
gas_block = int(re.findall('Hard gas limit per block: (\d+)', data)[0])
storage_op = int(re.findall('Hard storage limit per operation: (\d+)', data)[0])
reward_slot = int(re.findall('Endorsing reward per slot: (\d+)', data)[0])
delay = int(re.findall('Minimal block delay: (\d+)', data)[0])
punishment = int(re.findall('Double baking punishment: (\d+)', data)[0])
threshold = int(re.findall('Consensus threshold: (\d+)', data)[0])
requirement = re.findall('Requirement: (\w+)', data)[0]
balances = {}
balance_regex = re.compile(r'([\w-]+):\n\s+key:\s+(\w+)\n\s+is_bootstrap_baker_account:\s+(true|false)\n\s+bootstrap_balance:\s+\'(\d+)\'')
for match in balance_regex.finditer(data):
    node_name = match.group(1)
    balance = int(match.group(4))
    balances[node_name] = balance
print(balances)


# xtract the relevant information 
# (storage size, memory, cpu, instances), 
# calculate the capacity for each node
node_capacity = []
for node in nodes.values():
    storage_size = node.get('storage_size', 0)
    memory = node.get('resources', {}).get('requests', {}).get('memory', 0)
    cpu = node.get('resources', {}).get('requests', {}).get('cpu', 0)
    instances = node.get('instances', 1)
    capacity = (storage_size + memory + cpu) / instances
    node_capacity.append(capacity)
# Calculate average balance per node
avg_balance_per_node = sum(balances.values()) / len(balances)


# Group variables into features
block_size = np.array([gas_op, gas_block, storage_op])
finance = np.array([avg_balance_per_node, reward_slot, punishment])
node_capacity = np.array(node_capacity)
requirement_feature = np.array([1 if requirement == 'safety' else 0])

# Scale features
block_size_scaled = (block_size - block_size.mean()) / block_size.std()
finance_scaled = (finance - finance.mean()) / finance.std()
node_capacity_scaled = (node_capacity - node_capacity.mean()) / node_capacity.std()

# Concatenate features into state vector
state = np.concatenate([block_size_scaled, finance_scaled, node_capacity_scaled, requirement_feature])

print(state)