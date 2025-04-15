import random

def generate_company_data(min_budget, max_budget, max_interest, max_grace, n=20):
    companies = []

    for i in range(n):
        budget = random.randint(min_budget, max_budget)
        interest = round(random.uniform(10, max_interest), 2)
        grace = random.randint(3, max_grace)
        company = {
            "name": f"PME_{i+1}",
            "budget": budget,
            "classical_interest": interest,
            "prosac_grace": grace,
        }
        companies.append(company)

    return companies
