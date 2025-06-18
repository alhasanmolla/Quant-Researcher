# 📁 rl_agent/trading_env.py

import gymnasium as gym
from gymnasium import spaces
import pandas as pd
import numpy as np

class TradingEnv(gym.Env):
    def __init__(self, df):
        super(TradingEnv, self).__init__()
        self.df = df.reset_index(drop=True)
        self.n_steps = len(df)
        self.current_step = 0
        self.balance = 10000  # initial cash
        self.position = 0     # holding stock
        self.total_profit = 0
        self.initial_balance = self.balance
        self.portfolio_value = self.balance

        self.action_space = spaces.Discrete(3)  # 0: Hold, 1: Buy, 2: Sell
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(df.shape[1],), dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        self.balance = self.initial_balance
        self.position = 0
        self.total_profit = 0
        self.portfolio_value = self.balance
        return self._next_observation(), {}

    def _next_observation(self):
        return self.df.iloc[self.current_step].values.astype(np.float32)

    def step(self, action):
        current_price = self.df.iloc[self.current_step]['Close']
        done = False
        reward = 0

        # Buy
        if action == 1 and self.balance >= current_price:
            self.position += 1
            self.balance -= current_price

        # Sell
        elif action == 2 and self.position > 0:
            self.position -= 1
            self.balance += current_price

        # Calculate portfolio value and reward
        prev_portfolio_value = self.portfolio_value
        self.portfolio_value = self.balance + self.position * current_price
        reward = self.portfolio_value - prev_portfolio_value

        # Update total profit
        self.total_profit = self.portfolio_value - self.initial_balance

        # Small penalty for holding to encourage decision-making, but only if not at the beginning
        if action == 0 and self.current_step > 0:
            reward -= 1

        self.current_step += 1
        if self.current_step >= self.n_steps - 1:
            done = True

        obs = self._next_observation()
        truncated = False # Assuming no truncation for now
        return obs, reward, done, truncated, {}

    def render(self, mode='human'):
        print(f"Step: {self.current_step}, Balance: {self.balance}, Position: {self.position}, Total Profit: {self.total_profit}")
