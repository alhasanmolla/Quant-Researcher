# 📁 rl_agent/train_agent.py

import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from trading_env import TradingEnv

# Step 1: Load Data
df = pd.read_csv("final_dataset.csv")
df = df[['Close', 'Volume', 'RSI', 'MACD', 'OBV', 'SentimentScore']]

# Step 2: Create environment
env = TradingEnv(df)
check_env(env)  # optional: for debugging

# Step 3: Train PPO Agent
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# Save the model
model.save("ppo_trading_agent")
