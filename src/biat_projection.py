import numpy as np
from repayment_model import simulate_repayment

def simulate_biat_returns(all_company_simulations, loan_amount=100000, interest_rate=0.07):
    full_distribution = []

    for simulations in all_company_simulations.values():
        for sim in simulations:
            repayments = simulate_repayment(sim, loan_amount, interest_rate)
            full_distribution.append(repayments)

    average = np.mean(full_distribution, axis=0)
    return average, full_distribution
