import os

import gym
import numpy as np
import matplotlib.pyplot as plt

from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import load_results, ts2xy
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3 import A2C, SAC, DDPG
from stable_baselines3.common import results_plotter
from stable_baselines3.common.evaluation import evaluate_policy

from env import MyEnvironment # import your custom environment
from state import process_state 

MEMORY_MAX =  1073741824 #1024Mi
CPU_MAX = 1000000000 #1000M
MEMORY_MIN = 33554432 #32Mi
CPU_MIN = 150000000 #150M

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

models_dir = "models/SAC"
logdir = "logs"
log_dir = "log_dir/SAC"

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

model = SAC('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

episode_blocks = []
throughput = []

TIMESTEPS = 100
for i in range(16):
    # Train the agent
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="SAC", callback=callback)
    # Save the agent
    model.save(f"{models_dir}/{TIMESTEPS*i}")


# # Plot balance and reward

fig, ax = plt.subplots()
# ax.set_ylabel('Reward')
# ax.plot(env.reward_history, color='b')
# ax.tick_params(axis='y', labelcolor='b')

# # Highlight reward range
# reward_min = 0.00005 * env.balance_history[-1]
# reward_max = 0.0005 * env.balance_history[-1]
# ax.fill_between(range(len(env.reward_history)), reward_min, reward_max, color='orange', alpha=0.3)

# fig.tight_layout()

# # Save the figure
# fig.savefig("./figures/balance.png")
# plt.close(fig)

# # Scatter plot 1: block size vs memory
# fig, ax = plt.subplots()
# ax.scatter(env.block_size_history, env.memory_history)

# # Add labels and title
# ax.set_xlabel('Block Size')
# ax.set_ylabel('Memory')
# ax.set_title('Block Size vs. Memory')
# colors = np.where(env.block_size_history > env.memory_history, 'r', 'b')

# plt.show()
# # Save the figure
# fig.savefig("./figures/ddpg_block_size_memory.png")
# plt.close(fig)

# # Scatter plot 2: block size vs cpu
# fig, ax = plt.subplots()
# ax.scatter(env.block_size_history, env.cpu_history)

# # Add labels and title
# ax.set_xlabel('Block Size')
# ax.set_ylabel('CPU')
# ax.set_title('Block Size vs. CPU')
# colors = np.where(env.block_size_history > env.cpu_history, 'r', 'b')

# plt.show()
# # Save the figure
# fig.savefig("./figures/ddpg_block_size_cpu.png")
# plt.close(fig)


# # plot 3: Requirement
# # Assign labels
# labels = ['Emmy+' if x == 0 else 'Tenderbake' for x in env.requirement_history]
# print(env.requirement_history)
# env.requirement_history[0] = 0
# # Create plot
# plt.plot(env.requirement_history)
# plt.xlabel('Episodes')
# plt.ylabel('Requirement')

# plt.show()
# # # Save the figure
# fig.savefig("./figures/ddpg_requirement.png")
# plt.close(fig)

# #plot 4: number of required nodes
# num_nodes_history = []

# for cpu in env.cpu_history:
#     num_nodes = cpu / CPU_MIN
#     num_nodes_history.append(num_nodes)
# # Create plot
# plt.plot(num_nodes_history)
# plt.xlabel('CPU')
# plt.ylabel('Shard size')

# plt.show()
# # # Save the figure
# fig.savefig("./figures/ddpg_num_nodes.png")
# plt.close(fig)

#plot 5: block size
block_sizes_mb = [size / 1000000 for size in env.block_size_history]
# Create plot
plt.plot(block_sizes_mb, label="Dynamic sharding-based blockchain")
plt.xlabel('Episodes')
plt.ylabel('Block size(MB)')
# Add a horizontal line at y=346
plt.axhline(y=5.2, color='y', linestyle='-', label="Tezos blockchain")
plt.show()
# # Save the figure
fig.savefig("./figures/SAC_block_size.png")
plt.close(fig)

