import numpy as np
import random

def simulate_repayment(profit_path, loan_amount=1000, interest_rate=0.05, repayment_years=5):
    total_due = loan_amount * (1 + interest_rate)
    annual_payment = total_due / repayment_years
    repayments = []
    missed_years = 0
    defaulted = False

    for profit in profit_path:
        if defaulted:
            repayments.append(0)
            continue

        if profit < 8000:
            missed_years += 1
            repayment = 0
        else:
            if random.random() < 0.15:
                repayment = 0
                missed_years += 1
            else:
                repayment = min(profit * 0.3, annual_payment)

       
        if missed_years >= 2:
            defaulted = True

        repayments.append(repayment)

    return repayments
