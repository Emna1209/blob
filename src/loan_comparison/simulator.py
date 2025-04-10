import numpy as np
import random

def simulate_loan_scenarios(base_profit, years=10):
    return {
        "prosac": simulate(base_profit, loan_type="prosac", years=years),
        "classic": simulate(base_profit, loan_type="classic", years=years)
    }

def simulate(base, loan_type, years):
    profits = []
    repayments = []
    defaulted = False
    total_due = 10000  # fixed loan for test

    if loan_type == "prosac":
        interest = 0.08
        grant = 0.14
        grace = 3
        default_chance = 0.03
        growth_range = (0.08, 0.15)
    else:
        interest = 0.11
        grant = 0.0
        grace = 1
        default_chance = 0.08
        growth_range = (0.02, 0.07)

    total_repay = total_due * (1 - grant) * (1 + interest)
    annual_repay = total_repay / (years - grace)

    for year in range(years):
        # simulate profit
        growth = random.uniform(*growth_range)
        base *= (1 + growth)
        profits.append(base)

        # simulate repayment
        if defaulted:
            repayments.append(0)
        elif year < grace:
            repayments.append(0)
        elif random.random() < default_chance:
            defaulted = True
            repayments.append(0)
        else:
            repayments.append(min(annual_repay, base * 0.3))  # can't pay more than 30% profit

    return {
        "profits": profits,
        "repayments": repayments
    }
