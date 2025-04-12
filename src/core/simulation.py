import numpy as np
import random
from .config import YEARS

def simulate_profit_growth(start_profit, years=YEARS, growth_range=(0.03, 0.12)):
    path = []
    profit = start_profit
    for _ in range(years):
        growth = random.uniform(*growth_range)
        profit *= (1 + growth)
        path.append(profit)
    return path

def simulate_multiple_growth_paths(start_profit, n_simulations, **kwargs):
    return [simulate_profit_growth(start_profit, **kwargs) for _ in range(n_simulations)]
