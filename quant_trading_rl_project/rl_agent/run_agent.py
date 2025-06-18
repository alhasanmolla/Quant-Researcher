# 📁 rl_agent/run_agent.py

import pandas as pd
from trading_env import TradingEnv
from stable_baselines3 import PPO

# Load Data
df = pd.read_csv("final_dataset.csv")
df = df[['Close', 'Volume', 'RSI', 'MACD', 'OBV', 'SentimentScore']]

# Load trained agent
env = TradingEnv(df)
model = PPO.load("ppo_trading_agent")

obs, _ = env.reset()
for _ in range(len(df) - 1):
    action, _states = model.predict(obs)
    obs, reward, done, truncated, _ = env.step(action)
    done = done or truncated
    env.render()
    if done:
        break
