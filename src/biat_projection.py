import numpy as np
import random

def simulate_biat_group_returns(group_simulations, loan_amount, interest_rate, group_type):
    full_distribution = []

    # Risk tuning
    if group_type == "stable":
        miss_chance = 0.05
        default_chance = 0.005
    else:
        miss_chance = 0.15
        default_chance = 0.03

    for simulations in group_simulations.values():
        for profit_path in simulations:
            repaid = []
            defaulted = False
            for _ in profit_path:
                if defaulted:
                    repaid.append(repaid[-1] if repaid else 0)
                    continue
                if random.random() < default_chance:
                    defaulted = True
                    repaid.append(repaid[-1] if repaid else 0)
                elif random.random() < miss_chance:
                    repaid.append(repaid[-1] if repaid else 0)
                else:
                    next_val = (repaid[-1] if repaid else 0) + 1 / len(profit_path)
                    repaid.append(min(1.0, next_val))
            full_distribution.append(repaid)

    avg = np.mean(full_distribution, axis=0)
    return avg, full_distribution
