import matplotlib.pyplot as plt
from stable_baselines import A2C, SAC, DDPG
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.evaluation import evaluate_policy
from env import MyEnvironment # import your custom environment
from state import process_state 
import os

models_dir = "models/SAC"
logdir = "logs"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

# Create the environment
env = MyEnvironment(process_state())

model = SAC('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

TIMESTEPS = 10000
iters = 0
for i in range(30):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="SAC")
    model.save(f"{models_dir}/{TIMESTEPS*i}")
    
env.close()