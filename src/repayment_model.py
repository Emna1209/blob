import numpy as np

def simulate_repayment(profit_path, loan_amount=100000, interest_rate=0.07, repayment_years=5):
    total_due = loan_amount * (1 + interest_rate)
    annual_payment = total_due / repayment_years
    repayments = []

    for year_profit in profit_path:
        max_affordable = year_profit * 0.3
        paid = min(max_affordable, annual_payment)
        repayments.append(paid)

    return repayments
