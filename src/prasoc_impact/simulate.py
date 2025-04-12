import pandas as pd
from core.simulation import simulate_multiple_growth_paths
from core.repayment import simulate_repayment
from core.config import N_SIMULATIONS

def run_prasoc_simulations(df, loan_amount, interest_rate, years):
    results = []
    for _, row in df.iterrows():
        company = row["Nom PME"]
        income = row["Résultat net (TND)"]
        profit_paths = simulate_multiple_growth_paths(income, N_SIMULATIONS, years=years)

        for path in profit_paths:
            repayment_path = simulate_repayment(path, loan_amount, interest_rate)
            results.append({
                "company": company,
                "profit_path": path,
                "repayment_path": repayment_path,
                "total_repaid": sum(repayment_path),
                "defaulted": sum(repayment_path) < loan_amount * 0.6  # arbitrary threshold
            })
    return results