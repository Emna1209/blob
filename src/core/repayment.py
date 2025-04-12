from .config import GRACE_PRASOC, INTEREST_PRASOC, GRANT_RATE, YEARS, MAX_REPAY_RATIO
import random
def simulate_repayment(profit_path, loan_amount=100000, interest_rate=INTEREST_PRASOC, grace=GRACE_PRASOC,
                       default_chance=0.03, miss_chance=0.1, grant_rate=GRANT_RATE):
    total_due = loan_amount * (1 - grant_rate) * (1 + interest_rate)
    annual_payment = total_due / (YEARS - grace)

    repayments = []
    defaulted = False
    missed_years = 0

    for i, profit in enumerate(profit_path):
        if i < grace:
            repayments.append(0)
            continue

        if defaulted:
            repayments.append(0)
            continue

        if random.random() < default_chance:
            defaulted = True
            repayments.append(0)
            continue

        if random.random() < miss_chance:
            missed_years += 1
            repayments.append(0)
        else:
            pay = min(profit * MAX_REPAY_RATIO, annual_payment)
            repayments.append(pay)

    return repayments
