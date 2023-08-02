import os
import subprocess

import gym
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import load_results, ts2xy
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3 import A2C, SAC, DDPG
from stable_baselines3.common import results_plotter
from stable_baselines3.common.evaluation import evaluate_policy

from env import MyEnvironment # import your custom environment
from state import process_state 

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

def get_state(state):
    d = dict()
    d["num_nodes"] = int(((state[7] + 1) / 2) * (MAX_NUM_NODES - MIN_NUM_NODES) + MIN_NUM_NODES)
    d["block_size"] = ((state[1] + 1) / 2) * (BLOCK_SIZE_MAX - BLOCK_SIZE_MIN) + BLOCK_SIZE_MIN
    d["avg_balance"] = ((state[1] + 1) / 2) * (BALANCE_MAX - BALANCE_MIN) + BALANCE_MIN
    d["reward_block"] = ((state[2] + 1) / 2) * (REWARD_MAX - REWARD_MIN) + REWARD_MIN
    d["punishment"] = ((state[3] + 1) / 2) * (PUNISHMENT_MAX - PUNISHMENT_MIN) + PUNISHMENT_MIN 
    d["tps"] = d["block_size"] / (AVERAGE_TRANSACTION_COST * TIME_PER_BLOCK)
    return d

class SaveOnBestTrainingRewardCallback(BaseCallback):
    """
    Callback for saving a model (the check is done every ``check_freq`` steps)
    based on the training reward (in practice, we recommend using ``EvalCallback``).

    :param check_freq: (int)
    :param log_dir: (str) Path to the folder where the model will be saved.
      It must contains the file created by the ``Monitor`` wrapper.
    :param verbose: (int)
    """

    def __init__(self, check_freq: int, log_dir: str, verbose=1):
        super().__init__(verbose)
        self.check_freq = check_freq
        self.log_dir = log_dir
        self.save_path = os.path.join(log_dir, "best_model")
        self.best_mean_reward = -np.inf

    def _init_callback(self) -> None:
        # Create folder if needed
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:

            # Retrieve training reward
            x, y = ts2xy(load_results(self.log_dir), "timesteps")
            if len(x) > 0:
                # Mean training reward over the last 100 episodes
                mean_reward = np.mean(y[-100:])
                if self.verbose > 0:
                    print(f"Num timesteps: {self.num_timesteps}")
                    print(
                        f"Best mean reward: {self.best_mean_reward:.2f} - Last mean reward per episode: {mean_reward:.2f}"
                    )

                # New best model, you could save the agent here
                if mean_reward > self.best_mean_reward:
                    self.best_mean_reward = mean_reward
                    # Example for saving best model
                    if self.verbose > 0:
                        print(f"Saving new best model to {self.save_path}.zip")
                    self.model.save(self.save_path)

        return True

models_dir = "models/DDPG"
logdir = "logs"
log_dir = "log_dir/DDPG"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Create the environment
env = MyEnvironment(process_state())

# Logs will be saved in log_dir/monitor.csv
env = Monitor(env, log_dir)

# Create the callback: check every 1000 steps
callback = SaveOnBestTrainingRewardCallback(check_freq=1000, log_dir=log_dir)

model = DDPG('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

episode_blocks = []
throughput = []

TIMESTEPS = 100
for i in range(16):
    # Train the agent
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="DDPG", callback=callback)
    # Save the agent
    model.save(f"{models_dir}/{TIMESTEPS*i}")

state = get_state(env.state)
print(state)




fig, ax = plt.subplots()

# Plot Number of Nodes (Blue Line)
ax.set_ylabel('Nodes')
ax.set_xlabel('Episodes')
ax.plot(env.num_nodes_history, color='b', label='Number of nodes')
ax.tick_params(axis='y', labelcolor='b')

# Highlight Malicious Node Range (Orange Gap)
node_min = []
node_max = []
print(env.num_nodes_history, env.malicious_nodes_history)
for i in range(len(env.num_nodes_history)):
    node_min.append(3 * env.malicious_nodes_history[i])  # Assuming 1/3 of the nodes are malicious
    node_max.append(100)  # Dynamic upper boundary based on the maximum number of nodes

ax.fill_between(range(len(env.num_nodes_history)), node_min, node_max, color='orange', alpha=0.3, label='Accepted Node Range')
# The orange area represents the range of malicious nodes based on the assumption that 1/3 of the nodes are malicious.
# The bottom of the orange area corresponds to 1/3 of the total number of nodes at each episode,
# and the top of the orange area corresponds to the maximum number of nodes observed in the data.

fig.tight_layout()
plt.legend()  # Show legend for the plot elements
plt.show()
# Save the figure
fig.savefig("./figures/malicious_nodes.png")
plt.close(fig)
