import os
import subprocess

import gymnasium as gym
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
from utils.log import log

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

def run_algo(chain_name):
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    if not os.path.exists(logdir):
        os.makedirs(logdir)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create the environment
    env = MyEnvironment(process_state(chain_name))

    # Logs will be saved in log_dir/monitor.csv
    env = Monitor(env, log_dir)

    # Create the callback: check every 1000 steps
    callback = SaveOnBestTrainingRewardCallback(check_freq=1000, log_dir=log_dir)

    model = DDPG('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

    TIMESTEPS = 100
    for i in range(16):
        # Train the agent

        model.learn(total_timesteps=TIMESTEPS)
        # Save the agent
        # model.save(f"{models_dir}/{TIMESTEPS*i}")

    state = get_state(env.state)

    # Define the command
    config_file = f"{chain_name}_values.yaml"
    
    node_command = ['./script/generate_values.sh', '-b', '1', '-n', str(state['num_nodes']), '-c', chain_name]
    protocol_command = ['./script/protocol.sh', '-b', str(state['block_size']), '-p', str(state['punishment']), '-e', str(state['reward_block']), '-f', config_file]
    update_command =  [
        'helm', 'upgrade',
        chain_name, 'oxheadalpha/tezos-chain',
        '--values', f'./{chain_name}_values.yaml',
        '--namespace', chain_name
    ]

    # Run the command
    try:
        # Run the script
        log("Creating new config file", "INFO")
        subprocess.run(node_command, check=True)
        log("Creating new config file named " + config_file + " successfully!", "SUCCESS")
        try:
            # Run the script
            log("Updating protocol parameter for newly created config file", "INFO")
            subprocess.run(protocol_command, check=True)
            log("Updating protocol parameter for newly created config file successfully!", "SUCCESS")
            try:
                log("Updating " + chain_name + " with new protocol parameter" , "INFO")
                subprocess.run(update_command, check=True)
                log("Updating " + chain_name + " with new protocol parameter successfully" , "SUCCESS")
            except subprocess.CalledProcessError as e:
                log(f"Command failed: " + str(e), "ERROR")
        except subprocess.CalledProcessError as e:
            log(f"Command failed: " + str(e), "ERROR")
    except subprocess.CalledProcessError as e:
        log(f"Command failed " + str(e), "ERROR")

