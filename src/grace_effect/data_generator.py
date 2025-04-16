import random
import math

def generate_company_data(min_budget, max_budget, max_interest, max_grace, n=20):
    companies = []

    for i in range(n):
        # Lower initial budget to simulate loan need
        base_budget = int(random.randint(min_budget, max_budget) / 10)

        # Loan rounded to nearest 1,000
        raw_loan = random.randint(min_budget // 2, max_budget // 2)
        loan_amount = int(math.ceil(raw_loan / 1000.0) * 1000)

        total_budget = base_budget + loan_amount
        interest = random.randint(10, max_interest)
        grace = random.randint(3, max_grace)

        companies.append({
            "Company": f"PME_{i+1}",
            "Initial Budget": base_budget,
            "Loan Amount": loan_amount,
            "Total Budget": total_budget,
            "Classic Interest": interest,
            "PRASOC Grace": grace
        })

    return companies
