import numpy as np
import random

def simulate_growth_path(start_value, years=10, mean=0.06, std=0.15):
    values = []
    current = start_value
    for _ in range(years):
        growth = np.random.normal(mean, std)
        current *= max(0.5, 1 + growth)
        values.append(current)
    return values

def simulate_repayment_paths(start_profit, years, simulations, interest, grace, grant):
    paths = []
    loan_amount = 100000
    net_loan = loan_amount * (1 - grant)
    total_due = net_loan * (1 + interest)
    annual_payment = total_due / (years - grace)

    for _ in range(simulations):
        profit_path = simulate_growth_path(start_profit, years)
        repayment_path = []
        for i, profit in enumerate(profit_path):
            if i < grace:
                repayment_path.append(0)
            else:
                repayment_path.append(min(profit * 0.3, annual_payment))
        paths.append(repayment_path)

    return paths
