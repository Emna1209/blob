import random
import math

def generate_company_data(min_budget, max_budget, max_interest, max_grace, n=20):
    companies = []

    for i in range(n):
        # 1. Base budget (already owned)
        base_budget = random.randint(min_budget, max_budget)

        # 2. Loan amount, rounded to nearest 1,000
        raw_loan = random.randint(min_budget // 2, max_budget // 2)
        loan_amount = int(math.ceil(raw_loan / 1000.0) * 1000)

        # 3. Total budget = base + loan
        total_budget = base_budget + loan_amount

        interest = random.randint(10, max_interest)  # integer only
        grace = random.randint(3, max_grace)

        companies.append({
            "Nom PME": f"PME_{i+1}",
            "Budget Initial": base_budget,
            "Montant Crédit": loan_amount,
            "Budget Total": total_budget,
            "Taux Intérêt Classique": interest,
            "Période Grâce PRASOC": grace
        })

    return companies
