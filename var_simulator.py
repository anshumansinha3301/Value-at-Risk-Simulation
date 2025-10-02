#!/usr/bin/env python3
import random
import statistics
from typing import List, Dict

class PortfolioVaR:
    def __init__(self, portfolio_value: float, mean_return: float, volatility: float, days: int = 1):
        self.portfolio_value = portfolio_value
        self.mean_return = mean_return
        self.volatility = volatility
        self.days = days
        self.simulated_returns: List[float] = []

    def historical_simulation(self, returns: List[float], confidence: float = 0.95) -> float:
        sorted_returns = sorted(returns)
        index = int((1 - confidence) * len(sorted_returns))
        return round(self.portfolio_value * abs(sorted_returns[index]), 2)

    def variance_covariance_var(self, confidence: float = 0.95) -> float:
        from math import sqrt
        z_score = 1.65  # Approx for 95% confidence
        return round(self.portfolio_value * (self.volatility * sqrt(self.days)) * z_score, 2)

    def monte_carlo_var(self, simulations: int = 10000, confidence: float = 0.95) -> float:
        self.simulated_returns = []
        for _ in range(simulations):
            simulated_return = random.gauss(self.mean_return, self.volatility)
            self.simulated_returns.append(simulated_return)
        sorted_returns = sorted(self.simulated_returns)
        index = int((1 - confidence) * simulations)
        return round(self.portfolio_value * abs(sorted_returns[index]), 2)

    def summary(self, returns: List[float], confidence: float = 0.95) -> Dict[str, float]:
        return {
            "Historical VaR": self.historical_simulation(returns, confidence),
            "Variance-Covariance VaR": self.variance_covariance_var(confidence),
            "Monte Carlo VaR": self.monte_carlo_var(confidence=confidence)
        }

def demo():
    portfolio = PortfolioVaR(portfolio_value=100000, mean_return=0.001, volatility=0.02)
    historical_returns = [random.gauss(0.001,0.02) for _ in range(250)]  # 1-year daily returns
    print("Portfolio VaR Summary (95% confidence):")
    for k, v in portfolio.summary(historical_returns).items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    demo()
