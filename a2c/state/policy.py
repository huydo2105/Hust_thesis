# Extract node information
node_pattern = re.compile(r'(\w+)\n\s+(Storage size: [\d\.A-Z]+)\n((?:.|\n)*?)\n', re.MULTILINE)
nodes = {}
for match in node_pattern.finditer(data):
    node_name = match.group(1)
    storage_size_str = re.search('Storage size: ([\d\.A-Z]+)', match.group(2)).group(1)
    storage_size = parse_storage_size(storage_size_str)
    resources_str = match.group(3)
    cpu_str = re.search('cpu: "([\d\.]+)"', resources_str).group(1)
    cpu = float(cpu_str)
    memory_str = re.search('memory: "([\d\.A-Za-z]+)"', resources_str).group(1)
    memory = parse_memory_size(memory_str)
    nodes[node_name] = {'storage_size': storage_size, 'cpu': cpu, 'memory': memory}