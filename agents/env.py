import gym
import numpy as np
from stable_baselines3.common.env_checker import check_env
from state import process_state 
import random

REWARD_BLOCK_SIZE = 0.3
REWARD_FINANCE = 0.1
REWARD_NODE_CAPACITY = 0.2
REWARD_REQUIREMENT = 0.4
AVERAGE_TRANSACTION_COST = 1001
TIME_PER_BLOCK = 15

BLOCK_SIZE_MEAN = 6600000
MEMORY_MEAN = 52009369
CPU_MEAN = 575000000
BALANCE_MAX = 40000
BALANCE_MIN = 0
BLOCK_SIZE_MAX = 11200000
BLOCK_SIZE_MIN = 2000000
REWARD_MAX = 20
REWARD_MIN = 0.5
PUNISHMENT_MAX =  2000
PUNISHMENT_MIN = 5
MEMORY_MAX =  1073741824 #1024Mi
CPU_MAX = 1000000000 #1000M
MEMORY_MIN = 33554432 #32Mi
CPU_MIN = 150000000 #150M
MAX_NUM_NODES = 100 
MIN_NUM_NODES = 4

class MyEnvironment(gym.Env):
    def __init__(self, state):
        self.state = state  # Initialize the state
        self.malicious_nodes_history = []
        self.tps_history = []
        self.num_nodes_history = []
        self.block_size_history = []
        self.balance_history = []
        self.reward_history = []
        self.punishment_history = []
        self.memory_history = []
        self.cpu_history = []
        self.requirement_history = []
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(7,), dtype=np.float32)
        self.observation_space = gym.spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(8,),
            dtype=np.float32
        )
        
        
    def reset(self):
        # Reset the environment
        # Return the initial state as the observation
        self.state = process_state()
        self.state = self.state.astype(np.float32)
        return self.state

    def is_safe_shard(self, num_nodes, consensus):
        num_malicious_nodes = np.random.randint(1, 10)
        self.malicious_nodes_history.append(num_malicious_nodes)
        # Require liveness or consensus algorithm is Emmy plus
        if consensus == 0:
            committee_size = int(num_nodes * 1/2)
        # Require safety or consensus algorithm is Tenderbake
        else:
            committee_size = int(num_nodes * 1/3)
        if num_malicious_nodes >= committee_size:
            return False
        return True
    

    def is_valid_num_nodes(self, num_nodes):
        if num_nodes > MAX_NUM_NODES or num_nodes < MIN_NUM_NODES: 
            return False
        return True

    def is_valid_block_size(self, block_size):
        if block_size > BLOCK_SIZE_MAX or block_size < BLOCK_SIZE_MIN: 
            return False
        return True

    def is_valid_capacity(self, memory, cpu):
        if memory > MEMORY_MAX or memory < MEMORY_MIN: 
            return False
        if cpu > CPU_MAX or cpu < CPU_MIN: 
            return False
        return True

    def check_block_size(self, block_size):
        if block_size > BLOCK_SIZE_MEAN:
            return 1 # Block size is large
        return 0 # Block size is medium and small

    def check_memory_capacity(self, memory):
        if memory > MEMORY_MEAN:
            return 1; # Memory is good
        return 0 # Memory is medium and bad
        
    def check_cpu_capacity(self, cpu):
        if cpu > CPU_MEAN:
            return 1; # cpu is good
        return 0 # cpu is medium and bad

    def is_valid_balance(self, avg_balance, punishment, reward):
        if avg_balance < 0 or punishment < 0 or reward < 0:
            return False
        if avg_balance < BALANCE_MIN or avg_balance > BALANCE_MAX:
            return False
        if punishment < PUNISHMENT_MIN or punishment > PUNISHMENT_MAX:
            return False
        if reward < REWARD_MIN or reward > REWARD_MAX:
            return False    
        # Check if punishment are at least 1% or not larger than 15% of avg_balance_per_node
        if punishment < 0.01 * avg_balance or punishment > 0.3 * avg_balance:
            return False
        # Check if reward are at least 0.005% or not larger than 0.05% of avg_balance_per_node
        if reward < 0.00005 * avg_balance or reward > 0.0005 * avg_balance:
            return False
        return True

    def step(self, action):
        # Update state based on action
        new_state = self.update_state(action)
        new_state = new_state.astype(np.float32)

        # Calculate reward based on new state
        reward = self.calculate_reward(new_state)

        # Check if episode has ended
        done = self.check_if_done(new_state)

        # Update current state
        self.state = new_state
        num_nodes = int(((self.state[7] + 1) / 2) * (MAX_NUM_NODES - MIN_NUM_NODES) + MIN_NUM_NODES)
        block_size = ((self.state[1] + 1) / 2) * (BLOCK_SIZE_MAX - BLOCK_SIZE_MIN) + BLOCK_SIZE_MIN
        avg_balance = ((self.state[1] + 1) / 2) * (BALANCE_MAX - BALANCE_MIN) + BALANCE_MIN
        reward_block = ((self.state[2] + 1) / 2) * (REWARD_MAX - REWARD_MIN) + REWARD_MIN
        punishment = ((self.state[3] + 1) / 2) * (PUNISHMENT_MAX - PUNISHMENT_MIN) + PUNISHMENT_MIN
        memory = ((self.state[4] + 1) / 2) * (MEMORY_MAX - MEMORY_MIN) + MEMORY_MIN
        cpu = ((self.state[5] + 1) / 2) * (CPU_MAX - CPU_MIN) + CPU_MIN
        requirement = self.state[6]
        tps = block_size / (AVERAGE_TRANSACTION_COST * TIME_PER_BLOCK)
        self.tps_history.append(tps)
        self.num_nodes_history.append(num_nodes)
        self.block_size_history.append(block_size)
        self.balance_history.append(avg_balance)
        self.reward_history.append(reward_block)
        self.punishment_history.append(punishment)
        self.memory_history.append(memory)
        self.cpu_history.append(cpu)
        self.requirement_history.append(requirement)
        
        return new_state, reward, done, {}

    def get_history(self):
        return self.balance_history

    def update_state(self, action):
        # Scale the action values to the acceptable range
        num_nodes_action = action[6]
        block_size_action = action[0]
        finance_action = action[1:4]
        memory_action = action[4]
        cpu_action = action[5]
        num_nodes_scaled = np.clip(num_nodes_action, -1, 1)
        block_size_scaled = np.clip(block_size_action, -3, 3)
        finance_scaled = np.clip(finance_action, -1, 1)
        memory_scaled = np.clip(memory_action, -1, 1)
        cpu_scaled = np.clip(cpu_action, -1, 1)

        # Add the scaled values to the corresponding features of the current state
        new_num_nodes_scaled = self.state[7] + num_nodes_action
        new_block_size_scaled = self.state[0] + block_size_scaled
        new_finance_scaled = self.state[1:4] + finance_scaled
        new_memory_scaled = self.state[4] + memory_scaled
        new_cpu_scaled = self.state[5] + cpu_scaled
        new_requirement_feature = 1  # Updated according to self.state[6]

        # Update the state with the clipped feature values
        new_state = np.concatenate([[new_block_size_scaled], new_finance_scaled, [new_memory_scaled], [new_cpu_scaled], [new_requirement_feature], [new_num_nodes_scaled]])
        return new_state

    def calculate_reward(self, state, prev_state=None):
        # Calculate reward based on state
        # Unpack the state into features
        block_size_scaled = state[0]
        finance_scaled = state[1:4]
        memory_scaled = state[4]
        cpu_scaled = state[5]
        requirement_feature = state[6]
        num_nodes = state[7]
        # Get original value of block size and avg balance
        num_nodes = ((num_nodes + 1) / 2) * (MAX_NUM_NODES - MIN_NUM_NODES) + MIN_NUM_NODES
        block_size = ((block_size_scaled + 1) / 2) * (BLOCK_SIZE_MAX - BLOCK_SIZE_MIN) + BLOCK_SIZE_MIN
        avg_balance = ((finance_scaled[0] + 1) / 2) * (BALANCE_MAX - BALANCE_MIN) + BALANCE_MIN
        reward = ((finance_scaled[1] + 1) / 2) * (REWARD_MAX - REWARD_MIN) + REWARD_MIN
        punishment = ((finance_scaled[2] + 1) / 2) * (PUNISHMENT_MAX - PUNISHMENT_MIN) + PUNISHMENT_MIN
        memory = ((memory_scaled + 1) / 2) * (MEMORY_MAX - MEMORY_MIN) + MEMORY_MIN
        cpu = ((cpu_scaled + 1) / 2) * (CPU_MAX - CPU_MIN) + CPU_MIN
        # print("PUNISHMENT %s with AVG_BALANCE %s and CONDITION %s" % (punishment, avg_balance, punishment < 0.05 * avg_balance))
        # Calculate TPS
        tps = block_size / (AVERAGE_TRANSACTION_COST * TIME_PER_BLOCK)
        
        is_block_size_large = self.check_block_size(block_size)
        is_memory_good = self.check_memory_capacity(memory)
        is_cpu_good = self.check_cpu_capacity(cpu)

        # Check if tps is valid number
        if tps < 0:
            return 0

        if not self.is_safe_shard(num_nodes):
            return 0

        # if not self.is_valid_num_nodes(num_nodes):
        #     return 0

        # Check if punishment are at least 5% of avg_balance_per_node
        if not self.is_valid_balance(avg_balance, punishment, reward):
            return 0

        # Penalize sudden changes in block size
        if not self.is_valid_block_size(block_size):
            return 0

        # Penalize sudden changes in block size
        if not self.is_valid_capacity(memory, cpu):
            return 0


        if is_block_size_large and not is_memory_good and not is_cpu_good:
            return 0

        if not is_block_size_large and is_memory_good and is_cpu_good:
            return 0

        # Combine the rewards
        total_reward = tps

        # print("BLOCKS_SIZE: %s with TPS: %s"% (block_size, total_reward))
        return total_reward
    
    # def check_capacity()

    def check_if_done(self, state):
        # Check if episode has ended based on state
        # Unpack the state into features
        block_size_scaled = state[0]
        finance_scaled = state[1:4]
        memory_scaled = state[4]
        cpu_scaled = state[5]
        requirement_feature = state[6]
        num_nodes_scaled = state[7]

        num_nodes = ((num_nodes_scaled + 1) / 2) * (MAX_NUM_NODES - MIN_NUM_NODES) + MIN_NUM_NODES
        block_size = ((block_size_scaled + 1) / 2) * (BLOCK_SIZE_MAX - BLOCK_SIZE_MIN) + BLOCK_SIZE_MIN
        avg_balance = ((finance_scaled[0] + 1) / 2) * (BALANCE_MAX - BALANCE_MIN) + BALANCE_MIN
        reward = ((finance_scaled[1] + 1) / 2) * (REWARD_MAX - REWARD_MIN) + REWARD_MIN
        punishment = ((finance_scaled[2] + 1) / 2) * (PUNISHMENT_MAX - PUNISHMENT_MIN) + PUNISHMENT_MIN
        memory = ((memory_scaled + 1) / 2) * (MEMORY_MAX - MEMORY_MIN) + MEMORY_MIN
        cpu = ((cpu_scaled + 1) / 2) * (CPU_MAX - CPU_MIN) + CPU_MIN

        # Check if any feature is outside the acceptable range
        if not self.is_valid_num_nodes(num_nodes) or not self.is_valid_block_size(block_size) or not self.is_valid_balance(avg_balance, punishment, reward) or \
        not self.is_valid_capacity(memory, cpu) or not self.is_safe_shard(num_nodes, requirement_feature) or requirement_feature not in [0, 1]:
            return True
        else:
            return False


env = MyEnvironment(process_state())
# It will check your custom environment and output additional warnings if needed
check_env(env)
# Box(4,) means that it is a Vector with 4 components
print("Reset state space shape:", process_state().shape)
print("Observation space:", env.observation_space)
print("Shape:", env.observation_space.shape)
# Discrete(2) means that there is two discrete actions
print("Action space:", env.action_space)

# The reset method is called at the beginning of an episode
obs = env.reset()
# Sample a random action
action = env.action_space.sample()
print("Sampled action:", action)
obs, reward, done, info = env.step(action)
# Note the obs is a numpy array
# info is an empty dict for now but can contain any debugging info
# reward is a scalar
print(obs.shape, reward, done, info)